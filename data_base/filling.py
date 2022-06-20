from datetime import datetime, timedelta
import pandas as pd

from main import run, TIME_ZONE
from rates.bars import Rates
from db import Data_base, Session, engine
import models
from rates.indicators import Indicator


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
        first_bar = self.get_bars_range(datetime(1970, 1, 1, tzinfo=TIME_ZONE),
                            datetime(1970, 5,5, tzinfo=TIME_ZONE)
                            ) # даты выбраны любые (до полу года)
        try:
            date = first_bar["time"][0]
        except:
            print(f"Dataframe {self.symbol} пустой")
            return False
        return date

    def check_first_bar_for_d1(self, first_time):
        delta = timedelta(days=1)
        range_day = first_time + delta
        range_bars = self.get_bars_range(first_time, range_day)
        second_time = range_bars["time"][1]
        if second_time.hour or second_time.minute:
            return second_time
        return False

    def get_first_bar(self):
        desired_date = None
        first_bar = self.get_first_bar_for_d1()
        if first_bar.hour != 0 or first_bar.minute != 0:
            return first_bar
        else:
            second_bar = self.check_first_bar_for_d1(first_bar)
            if second_bar:
                return second_bar
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
        date_to = date_from + timedelta(weeks=5)
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
        while first_bar < datetime.now():
            range_bars = self.get_range(first_bar)
            with Session() as session:
                symbol = session.query(models.Symbols.id).filter(models.Symbols.symbol==self.symbol).one()[0]
            for bar in range_bars.itertuples(index=False):
                data_for_save = TIME_FRAME_TABLES[self.time_frame](symbol_id=symbol,
                                                                   datetime=bar.time,
                                                                   open=bar.open,
                                                                   high=bar.high,
                                                                   low=bar.low,
                                                                   close=bar.close,
                                                                   tick_volume=bar.tick_volume,
                                                                   real_volume=bar.real_volume,
                                                                   spread=bar.spread)
                bars.append(data_for_save)
            first_bar += timedelta(weeks=10)
        self.save_data_to_db(bars)

    def fill_symbol(self, group):
        from tst import SNP
        data = []
        with Session() as session:
            group_id = session.query(models.Groups.id).filter(models.Groups.group==group).one()[0]
        for sym in SNP:
            data_symb = models.Symbols(symbol=sym, name=SNP[sym], group_id=group_id)
            data.append(data_symb)
        self.save_data_to_db(data)

    def get_indicators(self):
        with Session() as session:
            table = TIME_FRAME_TABLES[self.time_frame]
            simbol_id = session.query(models.Symbols.id).filter(models.Symbols.symbol==self.symbol).one()[0]
            bars = session.query(table).filter(table.symbol_id==simbol_id).order_by(table.datetime).limit(150)
        df_bars = pd.read_sql(bars.statement, engine)
        df_bars.rename(columns = {'real_volume' : 'volume'}, inplace = True)
        indicators = Indicator(df_bars)
        df_bars_with_indicators = indicators.attach_indicators()
        return df_bars_with_indicators

    def save_indicators(self, indicators):
        data_for_save = []
        table = TIME_FRAME_TABLES[self.time_frame]
        with Session() as session:
            for row in indicators.itertuples(index=False):
                session.query(table).filter(table.id==row.id).update({"rsi": None, "mfi": None})
                session.commit()
                print("Complete")
                break




if __name__=="__main__":

    fil = Filling("MMM", "d1")
    fil.save_indicators(fil.get_indicators())
    # print(fil.check_first_bar_for_d1(first))










    # from tst import SNP
    # run()
    # for tf in SNP:
    #     print("***********************")
    #     print(f"Start {tf}")
    #     for sym in S:
    #         print(f"[ {sym} ]")
    #         fil = Filling(sym, tf)
    #         try:
    #             fil.save_bars_to_db()
    #         except Exception as ex:
    #             print(f"Not instrument {sym}!!!", ex)
