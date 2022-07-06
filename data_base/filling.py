from datetime import datetime, timedelta, date
from sqlalchemy.sql import func
import pandas as pd
from statistics import mean

from main import run, TIME_ZONE, get_session
from rates.bars import Rates
from db import Data_base
from utils.data import SNP, SNPP
from rates.indicators import Indicator
import models


TIME_FRAME_TABLES = {"d1": models.D1_bars,
                     "h2": models.H2_bars,
                     "h1": models.H1_bars,
                     "m30": models.M30_bars,
                     "m10": models.M10_bars,
                     "m5": models.M5_bars,
                     "m1": models.M1_bars,
                     }

class Filling(Rates, Data_base):

    def fill_instruments(self, group, session):
        data = []
        group_id = session.query(models.Groups.id).filter(models.Groups.group==group).one()[0]
        for sym in SNP:
            data_symb = models.Instruments(symbol=sym, name=SNP[sym], group_id=group_id)
            data.append(data_symb)
        self.save_data_to_db(data, session=session)
        return self


    def get_first_bar_for_d1(self):
        chance = 1
        first_bar = self.get_bars_range(datetime(1970, 1, 1, tzinfo=TIME_ZONE),
                            datetime(1970, 5,5, tzinfo=TIME_ZONE)
                            ) # даты выбраны любые (до полу года)
        if not first_bar.empty:
            date = first_bar["time"][0]
            return date
        elif first_bar.empty and chance < 4:
            chance += 1
            print(f"Dataframe {self.symbol} пустой. Шанс {chance}.")
            return self.get_first_bar_for_d1()
        else:
            print(f"Dataframe {self.symbol} пустой. Шанс {chance}. Все!!!")
            return False


    def check_first_bar(self, first_time):
        delta = timedelta(days=10)
        range_day = first_time + delta
        range_bars = self.get_bars_range(first_time, range_day)
        second_time = range_bars["time"][1]
        if second_time.hour or second_time.minute:
            return second_time
        return False


    def get_first_bar(self, session):
        if self.time_frame in ["h1", "m30", "m10"]:
            table = models.H2_bars # в периодах h1, m30, m10 начальные бары такие же
            symbol_id = session.query(models.Instruments.id).filter(models.Instruments.symbol==self.symbol).one()[0]
            bar_time = session.query(table.datetime).filter(table.instrument_id==symbol_id).order_by(table.datetime).first()[0]
            check_time = bar_time - timedelta(days=1)
            check_bar = self.check_first_bar(check_time)
            if check_bar:
                if check_bar.hour != 0 or check_bar.minute != 0:
                    return check_bar
        desired_date = None
        first_bar = self.get_first_bar_for_d1()
        attempt = 0
        if first_bar:
            if first_bar.hour != 0 or first_bar.minute != 0:
                return first_bar
            else:
                second_bar = self.check_first_bar(first_bar)
                if second_bar:
                    return second_bar
        else:
            attempt += 1
            if attempt < 3:
                self.get_first_bar(session)
        first_date = int(datetime(2000, 1, 1, tzinfo=TIME_ZONE).timestamp())
        curent_date = int(datetime.now().timestamp())
        later = True
        while not desired_date:
            center_date = (curent_date + first_date) // 2
            bars = self.get_bars_from(center_date, 100)
            time_bars = bars["time"]
            for i, time in enumerate(time_bars):
                if time.hour or time.minute:
                    if i > 1:
                        desired_date = time
                        break
                    else:
                        later = False
                        break
            if later:
                first_date = center_date
            else:
                curent_date = center_date
                later = True
        return desired_date


    def get_range(self, date_from):
        date_to = date_from + timedelta(weeks=10)
        if date_to > datetime.now():
            date_to = datetime.now()
        bars_range = self.get_bars_range(date_from, date_to)
        return bars_range


    def save_bars_to_db(self, session, first_bar=None, last_bar=datetime.now(), instrument_id=None):
        if not first_bar:
            if self.time_frame == "d1":
                first_bar = self.get_first_bar_for_d1()
            else:
                first_bar = self.get_first_bar(session)
        bars = []
        if not instrument_id:
            instrument_id = session.query(models.Instruments.id).filter(models.Instruments.symbol==self.symbol).one()[0]
        while first_bar < last_bar:
            range_bars = self.get_range(first_bar)[1:]
            for bar in range_bars.itertuples(index=False):
                data_for_save = TIME_FRAME_TABLES[self.time_frame](instrument_id=instrument_id,
                                                                    datetime=bar.time,
                                                                    open=round(bar.open, 2),
                                                                    high=round(bar.high, 2),
                                                                    low=round(bar.low, 2),
                                                                    close=round(bar.close, 2),
                                                                    tick_volume=bar.tick_volume,
                                                                    real_volume=bar.real_volume,
                                                                    spread=bar.spread
                                                                    )
                bars.append(data_for_save)
            first_bar += timedelta(weeks=10)
        self.save_data_to_db(bars, session)
        return len(bars)


    def get_indicators(self, session, count, table, symbol_id, delta):
        bars = session.query(table.id,
                             table.datetime,
                             table.open,
                             table.high,
                             table.low,
                             table.close,
                             table.real_volume).filter(table.instrument_id==symbol_id).order_by(table.datetime)[(count - delta):(count)]
        df_bars = pd.DataFrame(bars, columns=["id", "datetime", "open", "high", "low", "close", "volume"])
        indicators = Indicator(df_bars)
        df_bars_with_indicators = indicators.attach_indicators()
        return df_bars_with_indicators


    def save_indicators(self, session, count, table, symbol_id, delta=20035):
        indicators = self.get_indicators(session, count, table, symbol_id, delta)
        for row in indicators[34:].itertuples(index=False):
            session.query(table).filter(table.id==row.id).update({"rsi": row.rsi, "mfi": row.mfi, "ao": row.ao, "fisher": row.fisher})
        return self


    def fill_indicators(self, session):
        table = TIME_FRAME_TABLES[self.time_frame]
        instrument_id = session.query(models.Instruments.id).filter(models.Instruments.symbol==self.symbol).one()[0]
        count_bars = session.query(table).filter(table.instrument_id==instrument_id).count()
        count = 20035 # эта цифра используется для индикаторов, которые отдают результаты не
                # с первого бара(например АО дает результат только с 35) и + 20000 следующих баров
        if count > count_bars:
            count = count_bars
        while count <= (count_bars + 1):
            self.save_indicators(session, count, table, instrument_id)
            if (count + 20000) < count_bars:
                count += 20000
            else:
                delta = count_bars - count
                count = count_bars
                self.save_indicators(session, count, table, instrument_id, delta=delta)
                break
        return self


    @staticmethod
    def fill_avg_volume(session, symbol=None, instrument_id=None):
        table = models.D1_bars
        if not instrument_id:
            instrument_id = session.query(models.Instruments.id).filter(models.Instruments.symbol==symbol).one()[0]
        avg_volume = int(session.query(func.avg(table.real_volume)).filter(table.instrument_id == instrument_id).first()[0])
        month_vol = session.query(table.real_volume).filter(table.instrument_id == instrument_id).order_by(table.datetime.desc()).limit(30).all()
        avg_month_vol = int(mean([i[0] for i in month_vol]))
        session.query(models.Instruments).filter(models.Instruments.id==instrument_id).update({"avg_volume": avg_volume, "avg_volume_lm": avg_month_vol})
        return avg_volume


    @staticmethod
    def fill_atr_and_closing_price(session, symbol=None, instrument_id=None):
        table = models.D1_bars
        if not instrument_id:
            instrument_id = session.query(models.Instruments.id).filter(models.Instruments.symbol==symbol).one()[0]
        bars = session.query(table.id,
                        table.datetime,
                        table.open,
                        table.high,
                        table.low,
                        table.close).filter(table.instrument_id==instrument_id).order_by(table.datetime.desc()).limit(20)
        df_bars = pd.DataFrame(bars, columns=["id", "datetime", "open", "high", "low", "close"]).iloc[::-1]
        indicator = Indicator(df_bars)
        atr_df = indicator.get_atr()
        atr = atr_df.iloc[-1]
        closing_price = df_bars.close.iloc[-1]
        atr_percent = round((atr / closing_price * 100), 2)
        session.query(models.Instruments).filter(models.Instruments.id==instrument_id).update({"atr": atr, "atr_percent": atr_percent,"closing_price": closing_price})
        return atr


    def fill_all_last_changes(self):
        with get_session() as session:
            table = TIME_FRAME_TABLES[self.time_frame]
            instrument_id = session.query(models.Instruments.id).filter(models.Instruments.symbol==self.symbol).one()[0]
            first_dt_bar = session.query(table.datetime).filter(table.instrument_id==instrument_id).order_by(table.datetime.desc()).first()[0]
            count_new_bars = self.save_bars_to_db(session=session, first_bar=first_dt_bar, instrument_id=instrument_id)
        with get_session() as session:
            count_bars = session.query(table).filter(table.instrument_id==instrument_id).count()
            self.save_indicators(session, count=count_bars, table=table, symbol_id=instrument_id, delta=(count_new_bars + 35))
            if self.time_frame == "d1":
                Filling.fill_avg_volume(session, instrument_id=instrument_id)
                Filling.fill_atr_and_closing_price(session, instrument_id=instrument_id)
        return self

time = ["d1", "h2", "h1", "m30", "m10", "m5"]

def main():
    run()
    for tf in time:
        print("***********************")
        print(f"Start {tf}")
        for sym in SNP:
            # with get_session() as session:
            print(f"[ {sym} ]")
            fill = Filling(sym, tf)
            # try:
            fill.fill_all_last_changes()
            # except Exception as ex:
            #     print(f"{sym}!!!", ex)


if __name__=="__main__":
    run()
    # with get_session() as session:
        # data = Data_base.get_bars_from_db(session=session,
        #                            dt_from=datetime(2022, 6, 1, tzinfo=TIME_ZONE),
        #                            dt_to=datetime(2022, 7, 1, tzinfo=TIME_ZONE),
        #                            time_frame="d1",
        #                            symbol="MMM"
        #                            )
        # print([i.open for i in data])
    #     Filling.fill_avg_volume(session, instrument_id=2)
    #     Filling.fill_atr_and_closing_price(session, instrument_id=2)



    # run()
    # for tf in ["d1"]:
    #     print("***********************")
    #     print(f"Start {tf}")
    #     for sym in ["MMM"]:
    #         print(f"[ {sym} ]")
    #         fill = Filling(sym, tf)
    #         fill.fill_indicators()
        # fill = Filling("MMM", "d1")
        # fill.save_bars_to_db(session=session)

    # run()
    # for tf in TIME_FRAME_TABLES:
    #     print("***********************")
    #     print(f"Start {tf}")
        # for sym in SNP:
        #     print(f"[ {sym} ]")
        #     fill = Filling(sym, tf)
        #     try:
        #         fill.save_bars_to_db()
        #     except Exception as ex:
        #         print(f"{sym}!!!", ex)

    # print("INDICATORS!!!!!!!!!!!")

    # for tf in ["m30"]:
    #     print("***********************")
    #     print(f"Start {tf}")
    #     for sym in ["TRMB"]:
    #         print(f"[ {sym} ]")
    #         fill = Filling(sym, tf)
    #         try:
    #             fill.fill_indicators()
    #         except Exception as ex:
    #             print(f"{sym}!!!", ex)

    # print("VOLUMES!!!!!!!!!!!")

    # for tf in ["d1"]:
    #     print("***********************")
    #     print(f"Start {tf}")
    #     for sym in SNP:
    #         print(f"[ {sym} ]")
    #         fill = Filling(sym, tf)
    #         try:
    #             fill.fill_avg_volume()
    #         except Exception as ex:
    #             print(f"{sym}!!!", ex)

    # print("ATR!!!!!!")

    # for sym in SNP:
    #     print(f"[ {sym} ]")
    #     try:
    #         Filling.fill_atr_and_closing_price(sym)
    #     except Exception as ex:
    #         print(f"{sym}!!!", ex)
