import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from data_base.db import Data_base
from main import get_session
from visualization import Graphs
from rates.indicators import Indicator


class Testing_strategy():

    def __init__(self, session, instrument) -> None:
        self.session = session
        self.instrument = instrument
        self.fishers_limit = 2


    def get_bars_for_testing(self, time_frame):
        bars = Data_base.get_bars_from_db_all(self.session, self.instrument, time_frame)
        return bars

    def test_strategy(self):
        m30_bars = self.get_bars_for_testing("m30")
        first_bar = None
        second_bar = None
        previous_delta = timedelta(days=4)
        future_delta = timedelta(days=8)
        for bar in m30_bars.itertuples(index=False):
            if second_bar:
                if not np.isnan(bar.ao):
                    if second_bar.fisher > 1 and second_bar.fisher > bar.fisher and second_bar.fisher > first_bar.fisher and bar.rsi > 70 and h2_bars.mfi > 70:
                        h2_bars = Data_base.get_2bars_using_date(self.session, self.instrument, "d1", bar.datetime)
                        if h2_bars.iloc[1].fisher and h2_bars.iloc[0].fisher < h2_bars.iloc[1].fisher and h2_bars.iloc[0].fisher < self.fishers_limit and h2_bars.iloc[0].fisher > -self.fishers_limit:
                            print(f"Short first={first_bar.fisher}, second={second_bar.fisher}, curent={bar.fisher}, date={bar.datetime}")
                            print(f"early {h2_bars.iloc[1].datetime} fisher {h2_bars.iloc[1].fisher}; last {h2_bars.iloc[0].datetime} fisher {h2_bars.iloc[0].fisher}")
                            previous = bar.datetime - previous_delta
                            future = bar.datetime + future_delta
                            visual = Graphs(session=self.session, dt_from=previous, dt_to=future, time_frame="m30", symbol=self.instrument)
                            visual.create_graph()
                            pass
                    elif second_bar.fisher < -1 and second_bar.fisher < bar.fisher and second_bar.fisher < first_bar.fisher:
                        h2_bars = Data_base.get_2bars_using_date(self.session, self.instrument, "d1", bar.datetime)
                        if h2_bars.iloc[1].fisher and h2_bars.iloc[0].fisher > h2_bars.iloc[1].fisher and h2_bars.iloc[0].fisher < self.fishers_limit and h2_bars.iloc[0].fisher > -self.fishers_limit:
                            print(f"Long first={first_bar.fisher}, second={second_bar.fisher}, curent={bar.fisher}, date={bar.datetime}")
                            print(f"early {h2_bars.iloc[1].datetime} fisher {h2_bars.iloc[1].fisher}; last {h2_bars.iloc[0].datetime} fisher {h2_bars.iloc[0].fisher}")
                            previous = bar.datetime - previous_delta
                            future = bar.datetime + future_delta
                            visual = Graphs(session=self.session, dt_from=previous, dt_to=future, time_frame="m30", symbol=self.instrument)
                            visual.create_graph()
                            pass
                first_bar = second_bar
                second_bar = bar
            else:
                first_bar = second_bar
                second_bar = bar

    def check_formation_of_trend(self):
        d1_bars = self.get_bars_for_testing("d1")
        first_bar = None
        second_bar = None
        long_trend = []
        short_trend = []
        long = 0
        short = 0
        ao_list = []
        bars_for_atr = pd.DataFrame(columns=("open", "high", "low", "close", "volume"))
        # bars_for_atr = pd.DataFrame(columns=("datetime", "open", "high", "low", "close", "volume", "ao", "fisher", "rsi", "mfi"))
        atr = None
        for third_bar in d1_bars.itertuples(index=False):
            if len(bars_for_atr) < 16:
                bar = [third_bar.open, third_bar.high, third_bar.low, third_bar.close, third_bar.volume]
                bars_for_atr.loc[len(bars_for_atr.index)] = bar
            else:
                bar = [third_bar.open, third_bar.high, third_bar.low, third_bar.close, third_bar.volume]
                bars_for_atr.loc[bars_for_atr.index[-1] + 1] = bar
                indicator = Indicator(bars_for_atr)
                atr = indicator.get_atr().iloc[-1]
                bars_for_atr = bars_for_atr.iloc[1: , :]
            if not np.isnan(third_bar.ao):
                if len(ao_list) < 50:
                    ao_list.append(third_bar.ao)
                else:
                    ao_list.append(third_bar.ao)
                    ao_list.pop(0)
                    positive_ao = 0
                    negative_ao = 0
                    zero = 0
                    previous_ao = 0
                    pre_previous_ao = 0
                    for ao in ao_list:
                        if ao > 0 and previous_ao > 0:
                            positive_ao += 1
                        elif ao < 0 and previous_ao < 0:
                            negative_ao += 1
                        elif ao > 0 and previous_ao < 0:
                            positive_ao += 1
                            zero += 1
                        elif ao < 0 and previous_ao > 0:
                            negative_ao += 1
                            zero += 1
                        elif ao == 0:
                            pre_previous_ao = previous_ao
                        elif ao > 0 and previous_ao == 0 and pre_previous_ao > 0:
                            positive_ao += 1
                        elif ao < 0 and previous_ao == 0 and pre_previous_ao < 0:
                            negative_ao += 1
                        elif ao > 0 and previous_ao == 0 and pre_previous_ao < 0:
                            positive_ao += 1
                            zero += 1
                        elif ao < 0 and previous_ao == 0 and pre_previous_ao > 0:
                            negative_ao += 1
                            zero += 1
                        previous_ao = ao
                    delta = abs(positive_ao - negative_ao)
                    last_five = False
                    for index, ao in enumerate(ao_list[45:]):
                        if index == 0 and ao > 0:
                            last_five = "Positive"
                        elif index == 0 and ao < 0:
                            last_five = "Negative"
                        elif last_five and ao > 0 and ao_list[45:][index - 1] > 0:
                            last_five = "Positive"
                        elif last_five and ao < 0 and ao_list[45:][index - 1] < 0:
                            last_five = "Negative"
                        elif last_five and ao > 0 and ao_list[45:][index - 1] < 0:
                            last_five = False
                        elif last_five and ao < 0 and ao_list[45:][index - 1] > 0:
                            last_five = False
                    if positive_ao > negative_ao and delta > 20 and last_five == "Positive" and not short:
                        if long:
                            if third_bar.fisher > second_bar.fisher:
                                long += 1
                            # elif (second_bar.fisher - third_bar.fisher) < 0.2
                            else:
                                # if (second_bar.fisher - third_bar.fisher) < 0.2
                                long_trend[-1]["close"] = second_bar.open
                                long_trend[-1]["count"] = long
                                long = 0
                        else:
                            if second_bar.fisher < -self.fishers_limit and second_bar.fisher < first_bar.fisher and second_bar.fisher < third_bar.fisher:
                                long += 1
                                long_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        # print("long")
                    elif negative_ao > positive_ao and delta > 20 and last_five == "Negative" and not long:
                        if short:
                            if third_bar.fisher < second_bar.fisher:
                                short += 1
                            else:
                                short_trend[-1]["close"] = second_bar.open
                                short_trend[-1]["count"] = short
                                short = 0
                        else:
                            if second_bar.fisher > self.fishers_limit and second_bar.fisher > first_bar.fisher and second_bar.fisher > third_bar.fisher:
                                short += 1
                                short_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        # print("short")
                    elif positive_ao > negative_ao and delta > 20 and not last_five and not short:
                        if long:
                            if third_bar.fisher > second_bar.fisher:
                                long += 1
                            else:
                                long_trend[-1]["close"] = second_bar.open
                                long_trend[-1]["count"] = long
                                long = 0
                        else:
                            if second_bar.fisher < -self.fishers_limit and second_bar.fisher < first_bar.fisher and second_bar.fisher < third_bar.fisher:
                                long += 1
                                long_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        # print("long")
                    elif negative_ao > positive_ao and delta > 20 and not last_five and not long:
                        if short:
                            if third_bar.fisher < second_bar.fisher:
                                short += 1
                            else:
                                short_trend[-1]["close"] = second_bar.open
                                short_trend[-1]["count"] = short
                                short = 0
                        else:
                            if second_bar.fisher > self.fishers_limit and second_bar.fisher > first_bar.fisher and second_bar.fisher > third_bar.fisher:
                                short += 1
                                short_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        # print("short")
                    elif positive_ao > negative_ao and delta > 20 and last_five == "Negative":
                        if long:
                            if third_bar.fisher > second_bar.fisher:
                                long += 1
                            else:
                                long_trend[-1]["close"] = second_bar.open
                                long_trend[-1]["count"] = long
                                long = 0
                                if second_bar.fisher > self.fishers_limit and second_bar.fisher > first_bar.fisher and second_bar.fisher > third_bar.fisher:
                                    short += 1
                                    short_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        elif short:
                            if third_bar.fisher < second_bar.fisher:
                                short += 1
                            else:
                                short_trend[-1]["close"] = second_bar.open
                                short_trend[-1]["count"] = short
                                short = 0
                                if second_bar.fisher < -self.fishers_limit and second_bar.fisher < first_bar.fisher and second_bar.fisher < third_bar.fisher:
                                    long += 1
                                    long_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        else:
                            if second_bar.fisher < -self.fishers_limit and second_bar.fisher < first_bar.fisher and second_bar.fisher < third_bar.fisher:
                                long += 1
                                long_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                            elif second_bar.fisher > self.fishers_limit and second_bar.fisher > first_bar.fisher and second_bar.fisher > third_bar.fisher:
                                short += 1
                                short_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        # print("long short")
                    elif negative_ao > positive_ao and delta > 20 and last_five == "Positive":
                        if long:
                            if third_bar.fisher > second_bar.fisher:
                                long += 1
                            else:
                                long_trend[-1]["close"] = second_bar.open
                                long_trend[-1]["count"] = long
                                long = 0
                                if second_bar.fisher > self.fishers_limit and second_bar.fisher > first_bar.fisher and second_bar.fisher > third_bar.fisher:
                                    short += 1
                                    short_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        elif short:
                            if third_bar.fisher < second_bar.fisher:
                                short += 1
                            else:
                                short_trend[-1]["close"] = second_bar.open
                                short_trend[-1]["count"] = short
                                short = 0
                                if second_bar.fisher < -self.fishers_limit and second_bar.fisher < first_bar.fisher and second_bar.fisher < third_bar.fisher:
                                    long += 1
                                    long_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        else:
                            if second_bar.fisher < -self.fishers_limit and second_bar.fisher < first_bar.fisher and second_bar.fisher < third_bar.fisher:
                                long += 1
                                long_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                            elif second_bar.fisher > self.fishers_limit and second_bar.fisher > first_bar.fisher and second_bar.fisher > third_bar.fisher:
                                short += 1
                                short_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        # print("long short")
                    elif delta < 20 and zero >= 3:
                        if long:
                            if third_bar.fisher > second_bar.fisher:
                                long += 1
                            else:
                                long_trend[-1]["close"] = second_bar.open
                                long_trend[-1]["count"] = long
                                long = 0
                                if second_bar.fisher > self.fishers_limit and second_bar.fisher > first_bar.fisher and second_bar.fisher > third_bar.fisher:
                                    short += 1
                                    short_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        elif short:
                            if third_bar.fisher < second_bar.fisher:
                                short += 1
                            else:
                                short_trend[-1]["close"] = second_bar.open
                                short_trend[-1]["count"] = short
                                short = 0
                                if second_bar.fisher < -self.fishers_limit and second_bar.fisher < first_bar.fisher and second_bar.fisher < third_bar.fisher:
                                    long += 1
                                    long_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        else:
                            if second_bar.fisher < -self.fishers_limit and second_bar.fisher < first_bar.fisher and second_bar.fisher < third_bar.fisher:
                                long += 1
                                long_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                            elif second_bar.fisher > self.fishers_limit and second_bar.fisher > first_bar.fisher and second_bar.fisher > third_bar.fisher:
                                short += 1
                                short_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        # print("long short")
                    elif delta < 20 and zero < 3 and last_five == "Positive" and not short:
                        if long:
                            if third_bar.fisher > second_bar.fisher:
                                long += 1
                            else:
                                long_trend[-1]["close"] = second_bar.open
                                long_trend[-1]["count"] = long
                                long = 0
                        else:
                            if second_bar.fisher < -self.fishers_limit and second_bar.fisher < first_bar.fisher and second_bar.fisher < third_bar.fisher:
                                long += 1
                                long_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        # print("long")
                    elif delta < 20 and zero < 3 and last_five == "Negative" and not long:
                        if short:
                            if third_bar.fisher < second_bar.fisher:
                                short += 1
                            else:
                                short_trend[-1]["close"] = second_bar.open
                                short_trend[-1]["count"] = short
                                short = 0
                        else:
                            if second_bar.fisher > self.fishers_limit and second_bar.fisher > first_bar.fisher and second_bar.fisher > third_bar.fisher:
                                short += 1
                                short_trend.append({"date_open": third_bar.datetime, "open": third_bar.open})
                        # print("short")
                    elif long:
                        if third_bar.fisher > second_bar.fisher:
                            long += 1
                        else:
                            long_trend[-1]["close"] = second_bar.open
                            long_trend[-1]["count"] = long
                            long = 0
                            # ToDo Продумать if, когда при конце short или long может быть новый тренд.
                    elif short:
                        if third_bar.fisher < second_bar.fisher:
                            short += 1
                        else:
                            short_trend[-1]["close"] = second_bar.open
                            short_trend[-1]["count"] = short
                            short = 0
                            # ToDo Продумать if, когда при конце short или long может быть новый тренд.
            first_bar = second_bar
            second_bar = third_bar
        if not long_trend[-1].get("count"):
            long_trend.pop()
        if not short_trend[-1].get("count"):
            short_trend.pop()
        date_delta = timedelta(days=40)
        for i in long_trend:
            if i["count"] > 2:
                dt_from = i["date_open"] - date_delta
                dt_to = i["date_open"] + date_delta
                graph = Graphs(session, time_frame="d1", symbol=self.instrument, dt_from=dt_from, dt_to=dt_to)
                print(i["date_open"])
                graph.create_graph(date_entry=i["date_open"], entry=i["open"], type_order="long")
        sorted_long = self.sort_result_of_trend(long_trend)
        sorted_short = self.sort_result_of_trend(short_trend)
        print(f"long \n{sorted_long}")
        print(f"short \n{sorted_short}")


    def sort_result_of_trend(self, curent_trend):
        long_result = dict()
        for trend in curent_trend:
            if trend["count"] in long_result:
                long_result[trend["count"]] += 1
            else:
                long_result[trend["count"]] = 1
        sorted_long_trend = sorted(long_result.items())
        sorted_long_trend.reverse()
        sorted_long_trend = pd.DataFrame(sorted_long_trend, columns=("trend", "count"))
        count_long = 0
        chance_list = []
        for value in sorted_long_trend.itertuples(index=False):
            count_long += value.count
            chance_list.append(round((count_long / len(curent_trend) * 100)))
        sorted_long_trend["chance"] = chance_list
        return sorted_long_trend


if __name__=="__main__":
    with get_session() as session:
        test = Testing_strategy(session, "AOS")
        test.check_formation_of_trend()
