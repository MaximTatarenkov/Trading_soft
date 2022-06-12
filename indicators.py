import MetaTrader5 as mt5
from finta import TA
import pandas as pd


class Indicator:

    def __init__(self, symbol, bars_count, time_frame) -> None:
        self.symbol = symbol
        self.bars_count = bars_count
        self.time_frame = time_frame

    def get_bars(self):
        match self.time_frame:
            case "5m":
                bars = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M5, 0, self.bars_count)
            case "10m":
                bars = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M10, 0, self.bars_count)
            case "30m":
                bars = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M30, 0, self.bars_count)
            case "1h":
                bars = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M10, 0, self.bars_count)
            case "2h":
                bars = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M10, 0, self.bars_count)
            case "1d":
                bars = mt5.copy_rates_from_pos(self.symbol, mt5.TIMEFRAME_M10, 0, self.bars_count)
        data_frame_bars = pd.DataFrame(bars, columns=["time", "open", "high", "low", "close", "tick_volume", "spread", "real_volume"])
        data_frame_bars["time"] = pd.to_datetime(data_frame_bars["time"], unit="s")
        data_frame_bars.rename(columns = {'tick_volume' : 'volume'}, inplace = True)
        data_frame_bars.drop(["spread", "real_volume"], axis=1)
        return data_frame_bars

    def get_fisher(self):
        bars = self.get_bars()
        fish = TA.FISH(bars, 10)
        return fish
