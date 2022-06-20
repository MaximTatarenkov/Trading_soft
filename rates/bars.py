import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime


TIME_FRAME = {
    "m5": mt5.TIMEFRAME_M5,
    "m10": mt5.TIMEFRAME_M10,
    "m30": mt5.TIMEFRAME_M30,
    "h1": mt5.TIMEFRAME_H1,
    "h2": mt5.TIMEFRAME_H2,
    "d1": mt5.TIMEFRAME_D1,
}


class Rates:

    def __init__(
        self,
        symbol: str,
        time_frame: str,
        bars_count: str=None,
        date_from: datetime=None,
        date_to: datetime=None,
        start_pos: int=0,
        ) -> None:
        self.symbol = symbol
        self.bars_count = bars_count
        self.time_frame = time_frame
        self.date_from = date_from
        self.date_to = date_to
        self.start_pos = start_pos


    def get_bars_from_pos(self):
        """
        (symbol, time_frame, start_pos, bars_count)
        """
        bars = mt5.copy_rates_from_pos(self.symbol, TIME_FRAME[self.time_frame], self.start_pos, self.bars_count)
        data_frame_bars = self.convert_bars_to_df(bars)
        return data_frame_bars

    def get_bars_range(self, date_from=None, date_to=None):
        """
        (symbol, time_frame, date_from, date_to)
        """
        if not date_from:
            date_from = self.date_from
            date_to = self.date_to
        bars = mt5.copy_rates_range(self.symbol, TIME_FRAME[self.time_frame], date_from, date_to)
        data_frame_bars = self.convert_bars_to_df(bars)
        return data_frame_bars

    def get_bars_from(self, date_from=None, bars_count=None):
        """
        (symbol, time_frame, date_from, bars_count)
        """
        if not date_from:
            date_from = self.date_from
            bars_count = self.bars_count
        bars = mt5.copy_rates_from(self.symbol, TIME_FRAME[self.time_frame], date_from, bars_count)
        data_frame_bars = self.convert_bars_to_df(bars)
        return data_frame_bars

    def convert_bars_to_df(self, bars):
        data_frame_bars = pd.DataFrame(bars, columns=["time", "open", "high", "low", "close", "tick_volume", "spread", "real_volume"])
        data_frame_bars["time"] = pd.to_datetime(data_frame_bars["time"], unit="s")
        # data_frame_bars.rename(columns = {'tick_volume' : 'volume'}, inplace = True)
        # data_frame_bars = data_frame_bars.drop(["spread", "real_volume"], axis=1)
        return data_frame_bars
