from finta import TA


class Indicator:

    def __init__(self, bars, period: int=16) -> None:
        self.bars = bars
        self.period = period

    def get_fisher(self):
        fish = round(TA.FISH(self.bars, period=self.period), 2)
        return fish

    def get_ao(self):
        ao = round(TA.AO(self.bars), 2)
        return ao

    def get_rsi(self):
        rsi = round(TA.RSI(self.bars, period=self.period), 2)
        return rsi

    def get_mfi(self):
        mfi = round(TA.MFI(self.bars, period=self.period), 2)
        return mfi

    def get_atr(self):
        atr = round(TA.ATR(self.bars, period=self.period), 2)
        return atr

    # def attach_atr(self):
    #     atr = self.get_atr()
    #     self.bars["atr"] = atr
    #     return self.bars

    def attach_indicators(self):
        fisher = self.get_fisher()
        ao = self.get_ao()
        rsi = self.get_rsi()
        mfi = self.get_mfi()
        self.bars["fisher"], self.bars["ao"], self.bars["rsi"], self.bars["mfi"] = fisher, ao, rsi, mfi
        return self.bars
