from datetime import datetime, timedelta
import pandas as pd

from main import run, TIME_ZONE
from rates.bars import Rates
from db import Data_base, get_session, engine
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

    def get_first_bar(self):
        if self.time_frame in ["h1", "m30", "m10"]:
            with get_session() as session:
                table = models.H2_bars # в остальных периодах начальные бары такие же
                simbol_id = session.query(models.Symbols.id).filter(models.Symbols.symbol==self.symbol).one()[0]
                bar_time = session.query(table.datetime).filter(table.symbol_id==simbol_id).order_by(table.datetime).first()[0]
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
                self.get_first_bar()
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

    def save_bars_to_db(self):
        if self.time_frame == "d1":
            first_bar = self.get_first_bar_for_d1()
        else:
            first_bar = self.get_first_bar()
        bars = []
        with get_session() as session:
            symbol = session.query(models.Symbols.id).filter(models.Symbols.symbol==self.symbol).one()[0]
            while first_bar < datetime.now():
                range_bars = self.get_range(first_bar)
                for bar in range_bars.itertuples(index=False):
                    data_for_save = TIME_FRAME_TABLES[self.time_frame](symbol_id=symbol,
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

    @staticmethod
    def fill_symbol(group):
        data = []
        with get_session() as session:
            group_id = session.query(models.Groups.id).filter(models.Groups.group==group).one()[0]
            for sym in SNP:
                data_symb = models.Symbols(symbol=sym, name=SNP[sym], group_id=group_id)
                data.append(data_symb)
            Data_base.save_data_to_db(data, session)

    def get_indicators(self, session, count, table, simbol_id):
        bars = session.query(table.id,
                             table.datetime,
                             table.open,
                             table.high,
                             table.low,
                             table.close,
                             table.real_volume).filter(table.symbol_id==simbol_id).order_by(table.datetime)[(count - 135):(count)]
        df_bars = pd.DataFrame(bars, columns=["id", "datetime", "open", "high", "low", "close", "volume"])
        indicators = Indicator(df_bars)
        df_bars_with_indicators = indicators.attach_indicators()
        return df_bars_with_indicators

    def save_indicators(self, session, count, table, simbol_id):
        indicators = self.get_indicators(session, count, table, simbol_id)
        for row in indicators[34:].itertuples(index=False):
            session.query(table).filter(table.id==row.id).update({"rsi": row.rsi, "mfi": row.mfi, "ao": row.ao, "fisher": row.fisher})

    def fill_indicators(self):
        with get_session() as session:
            table = TIME_FRAME_TABLES[self.time_frame]
            simbol_id = session.query(models.Symbols.id).filter(models.Symbols.symbol==self.symbol).one()[0]
            count_bars = session.query(table).filter(table.symbol_id==simbol_id).count()
            count = 135 # эта цифра используется для индикаторов, которые отдают результаты не
                    # с первого бара(например АО дает результат только с 35) и + 100 следующих баров
            while count <= (count_bars + 1):
                self.save_indicators(session, count, table, simbol_id)
                if (count + 100) < count_bars:
                    count += 100
                else:
                    count = count_bars
                    self.save_indicators(session, count, table, simbol_id)
                    break

def main():
    for tf in ["m5"]:
        print("***********************")
        print(f"Start {tf}")
        for sym in ["MMM"]:
            print(f"[ {sym} ]")
            fill = Filling(sym, tf)
            try:
                fill.fill_indicators()
            except Exception as ex:
                print(f"{sym}!!!", ex)


if __name__=="__main__":
    main()

    # run()
    # for tf in ["d1"]:
    #     print("***********************")
    #     print(f"Start {tf}")
    #     for sym in ["MMM"]:
    #         print(f"[ {sym} ]")
    #         fill = Filling(sym, tf)
    #         fill.fill_indicators()

    # Filling.fill_symbol("S&P 500")

    # run()
    # for tf in TIME_FRAME_TABLES:
    #     print("***********************")
    #     print(f"Start {tf}")
    #     for sym in SNP:
    #         print(f"[ {sym} ]")
    #         fill = Filling(sym, tf)
    #         try:
    #             fill.save_bars_to_db()
    #         except Exception as ex:
    #             print(f"{sym}!!!", ex)

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
