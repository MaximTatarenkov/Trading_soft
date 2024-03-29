from matplotlib import pyplot as plt
from mpl_finance import candlestick2_ohlc
import pandas as pd
import datetime
import numpy as np
import matplotlib.ticker as ticker
from collections import namedtuple

from main import get_session
from data_base.db import Data_base


class Graphs():

    def __init__(self, session, dt_from, dt_to, time_frame, symbol) -> None:
        self.session = session
        self.dt_from = dt_from
        self.dt_to = dt_to
        self.time_frame = time_frame
        self.symbol = symbol

    def create_graph(self, entry=None, exit=None, date_entry=None, date_exit=None, type_order=None):
        fig, (ax_1, ax_2, ax_3, ax_4) = plt.subplots(4, 1, sharex=True, gridspec_kw={"height_ratios": [3, 1, 1, 1]})
        fig.patch.set_facecolor('k')
        fig.patch.set_alpha(0.6)

        ax_1.patch.set_facecolor('grey')
        ax_1.patch.set_alpha(1.0)
        ax_2.patch.set_facecolor('#778899')
        ax_2.patch.set_alpha(1.0)
        ax_3.patch.set_facecolor('#2F4F4F')
        ax_3.patch.set_alpha(1.0)
        ax_4.patch.set_facecolor('#FFE4E1')
        ax_4.patch.set_alpha(1.0)

        ax_1.grid(axis = "both")
        ax_2.grid(axis = "both")
        ax_3.grid(axis = "both")
        ax_4.grid(axis = "both")

        ax_1.minorticks_on()

        ax_1.grid(which='major',
                color = 'white',
                linewidth = 1)
        ax_1.grid(which='minor',
                color = 'white',
                linestyle = ':')
        ax_2.grid(which='major',
                color = 'k',
                linewidth = 1)
        ax_2.grid(which='minor',
                color = 'k',
                linestyle = ':')
        ax_3.grid(which='major',
                color = 'k',
                linewidth = 1)
        ax_3.grid(which='minor',
                color = 'k',
                linestyle = ':')
        ax_4.grid(which='major',
                color = 'k',
                linewidth = 1)
        ax_4.grid(which='minor',
                color = 'k',
                linestyle = ':')

        bars = self.get_bars_for_vizualization()
        dates = self.get_x_dates_and_flags(bars)
        position = np.arange(len(dates.x_dates))
        major_locator = self.get_major_locator(dates.flags)

        ax_1.set_xticks(position)
        ax_1.set_xticklabels(dates.x_dates, rotation = 45, horizontalalignment = 'left')
        ax_4.set_xticks(position)
        ax_4.set_xticklabels(dates.x_dates, rotation = 45, horizontalalignment = 'right')
        ax_1.xaxis.set_major_locator(ticker.MultipleLocator(major_locator))
        ax_1.xaxis.set_minor_locator(ticker.MultipleLocator(1))
        ax_2.xaxis.set_major_locator(ticker.MultipleLocator(major_locator))
        ax_2.xaxis.set_minor_locator(ticker.MultipleLocator(1))
        ax_3.xaxis.set_major_locator(ticker.MultipleLocator(major_locator))
        ax_3.xaxis.set_minor_locator(ticker.MultipleLocator(1))
        ax_4.xaxis.set_major_locator(ticker.MultipleLocator(major_locator))
        ax_4.xaxis.set_minor_locator(ticker.MultipleLocator(1))
        ax_1.tick_params(axis = 'both',    #  Применяем параметры к обеим осям
               which = 'major',    #  Применяем параметры к основным делениям
               direction = 'inout',    #  Рисуем деления внутри и снаружи графика
               length = 5,    #  Длинна делений
               width = 1,     #  Ширина делений
               labelsize = 10,    #  Размер подписи
               labelcolor = 'k',    #  Цвет подписи
               labelbottom = False,    #  Рисуем подписи снизу
               labeltop = True,    #  сверху
               labelleft = True,    #  слева
               labelright = False,    #  и справа
                )
        ax_2.tick_params(axis = 'both',    #  Применяем параметры к обеим осям
               which = 'major',    #  Применяем параметры к основным делениям
               direction = 'inout',    #  Рисуем деления внутри и снаружи графика
               length = 5,    #  Длинна делений
               width = 1,     #  Ширина делений
               labelsize = 10,    #  Размер подписи
               labelcolor = 'k',    #  Цвет подписи
               labelbottom = False,    #  Рисуем подписи снизу
               labeltop = False,    #  сверху
               labelleft = False,    #  слева
               labelright = True,    #  и справа
                )
        ax_3.tick_params(axis = 'both',    #  Применяем параметры к обеим осям
               which = 'major',    #  Применяем параметры к основным делениям
               direction = 'inout',    #  Рисуем деления внутри и снаружи графика
               length = 5,    #  Длинна делений
               width = 1,     #  Ширина делений
               labelsize = 10,    #  Размер подписи
               labelcolor = 'k',    #  Цвет подписи
               labelbottom = False,    #  Рисуем подписи снизу
               labeltop = False,    #  сверху
               labelleft = True,    #  слева
               labelright = False,    #  и справа
                )
        ax_4.tick_params(axis = 'both',    #  Применяем параметры к обеим осям
               which = 'major',    #  Применяем параметры к основным делениям
               direction = 'inout',    #  Рисуем деления внутри и снаружи графика
               length = 5,    #  Длинна делений
               width = 1,     #  Ширина делений
               color = 'm',    #  Цвет делений
               labelsize = 10,    #  Размер подписи
               labelcolor = 'k',    #  Цвет подписи
               bottom = True,    #  Рисуем метки снизу
               top = False,    #   сверху
               left = True,    #  слева
               right = False,    #  и справа
               labelbottom = True,    #  Рисуем подписи снизу
               labeltop = False,    #  сверху
               labelleft = False,    #  слева
               labelright = True,    #  и справа
                )

        ao = [i.ao for i in bars.df_bars.itertuples(index=False)]
        fisher = [i.fisher for i in bars.df_bars.itertuples(index=False)]
        rsi = [i.rsi for i in bars.df_bars.itertuples(index=False)]
        mfi = [i.mfi for i in bars.df_bars.itertuples(index=False)]
        candlestick2_ohlc(ax=ax_1,
                          opens=bars.df_bars['open'],
                          highs=bars.df_bars['high'],
                          lows=bars.df_bars['low'],
                          closes=bars.df_bars['close'],
                          width=0.6,
                          alpha=1,
                          colordown='red',
                          colorup='green',)
        ax_2.bar(np.arange(len(ao)), ao, color="#BA55D3", label="AO")
        ax_3.plot(np.arange(len(fisher)), fisher, color="#DC143C", label="Fish")
        ax_4.plot(np.arange(len(rsi)), rsi, color="#7B68EE", label="RSI")
        ax_4.plot(np.arange(len(rsi)), mfi, color="#FF7F50", label="MFI")


        if entry or exit:
            number_of_bar_and_max_min = self.get_number_of_bar_and_max_min(bars.db_bars, date_entry)
            number_entry = number_of_bar_and_max_min.date
            max_min = number_of_bar_and_max_min.max_min
            self.draw_entry_exit_points(type_order, ax_1, max_min, entry=entry, exit=exit, date_entry=number_entry, date_exit=date_exit)

        if date_entry:
            ax_1.legend(title = f"{self.symbol} {date_entry}")
        else:
            ax_1.legend(title = f"{self.symbol}")
        ax_2.legend()
        ax_3.legend()
        ax_4.legend()

        plt.subplots_adjust(wspace=0, hspace=0)
        plt.show()
        return self

    def get_bars_for_vizualization(self):
        bars = Data_base.get_bars_from_db_with_date(session=self.session,
                                dt_from=self.dt_from,
                                dt_to=self.dt_to,
                                time_frame=self.time_frame,
                                symbol=self.symbol
                                )
        bars = [bar[1:] for bar in bars]
        df_bars = pd.DataFrame(bars, columns=["datetime", "open", "high", "low", "close", "ao", "fisher", "rsi", "mfi"])
        df_bars = df_bars.sort_values("datetime")
        Bars = namedtuple("Bars", "db_bars df_bars")
        result = Bars(bars, df_bars)
        return result

    def get_number_of_bar_and_max_min(self, bars, date):
        max_min = {"max": 0, "min": 999999}
        for index, bar in enumerate(bars):
            if max_min["max"] < bar[2]:
                max_min["max"] = bar[2]
            if max_min["min"] > bar[3]:
                max_min["min"] = bar[3]
            if bar[0] == date:
                number_of_bar =  index
        Result = namedtuple("Result", "date max_min")
        result = Result(number_of_bar, max_min)
        return result

    def get_x_dates_and_flags(self, bars):
        dates = [i[0] for i in bars.db_bars]
        x_dates = []
        flags = []
        for i, date in enumerate(dates):
            if i == 0 or date.day != dates[i - 1].day:
                x_dates.append(date.strftime("%d %B %H:%M"))
                flags.append(i)
            else:
                x_dates.append(date.strftime("%d %B %H:%M"))
        Result = namedtuple("Result", "x_dates flags")
        result = Result(x_dates, flags[1:])
        return result

    def get_major_locator(self, flags):
        locators = [3, 4, 5]
        locs = []
        for loc in locators:
            for flag in flags:
                modul = flag % loc
                if not modul:
                    locs.append(loc)
        major_locator = 0
        count = 0
        for loc in locators:
            if locs.count(loc) > count:
                count = locs.count(loc)
                major_locator = loc
        return major_locator

    def draw_entry_exit_points(self, type_order, ax, max_min, entry=None, exit=None, date_entry=None, date_exit=None):
        range_price = max_min["max"] - max_min["min"]
        arrow_len = 0.1 * range_price
        if type_order == "long":
            arrow = arrow_len
        elif type_order == "short":
            arrow = -arrow_len
        if entry:
            ax.arrow(date_entry, entry - (2*arrow), 0, arrow,
            width = 0.2,
            head_length = arrow_len)
        if exit:
            ax.arrow(date_exit, exit + (2*arrow), 0, -arrow,
            width = 0.2,
            head_length = arrow_len)


if __name__ == "__main__":
    with get_session() as session:
        graph = Graphs(session, dt_from=datetime.datetime(1984, 7, 1), dt_to=datetime.datetime(1984, 10, 1), time_frame="d1", symbol="AOS")
        graph.create_graph()
