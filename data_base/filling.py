from datetime import datetime, timedelta

from main import run, TIME_ZONE
from rates.bars import Rates
from db import Data_base, Session
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
        old_year = 1970
        past_date = datetime(old_year, 1, 1, tzinfo=TIME_ZONE)
        first_bar = self.get_bars_from(past_date, 10)
        date = first_bar["time"][0]
        return date

    def get_first_bar(self):
        first_date = int(datetime(2000, 1, 1, tzinfo=TIME_ZONE).timestamp())
        curent_date = int(datetime.now().timestamp())
        desired_date = None
        later = True
        while not desired_date:
            center_date = (curent_date + first_date) // 2
            bars = self.get_bars_from(center_date, 10)
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
                                                                   volume=bar.volume)
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







if __name__=="__main__":

    run()
    fil = Filling("MMM", "h1")
    fil.get_first_bar()




# date_from = datetime(2011, 9, 30, tzinfo=TIME_ZONE)
# rates = Rates(symbol="BTCUSD", time_frame="m5", bars_count=50, date_from=date_from)
# bars = rates.get_bars_from()
# print(bars)
