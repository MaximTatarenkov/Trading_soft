from finta import TA


class Indicator:

    def __init__(self, bars, period: int=16) -> None:
        self.bars = bars
        self.period = period

    def get_fisher(self):
        fish = TA.FISH(self.bars, period=self.period)
        return fish

    def get_ao(self):
        ao = TA.AO(self.bars)
        return ao

    def get_rsi(self):
        rsi = TA.RSI(self.bars, period=self.period)
        return rsi

    def get_mfi(self):
        mfi = TA.MFI(self.bars, period=self.period)
        return mfi

    def attach_indicators(self):
        fish = self.get_fisher()
        ao = self.get_ao()
        rsi = self.get_rsi()
        mfi = self.get_mfi()
        self.bars["fish"], self.bars["ao"], self.bars["rsi"], self.bars["mfi"] = fish, ao, rsi, mfi
        return self.bars
