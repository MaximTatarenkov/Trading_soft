from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
from mpl_finance import candlestick2_ohlc
import pandas as pd
import datetime
import numpy as np
import matplotlib.ticker as ticker

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
        # ax_2.minorticks_on()
        # ax_3.minorticks_on()
        # ax_4.minorticks_on()

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

        bars = Data_base.get_bars_from_db(session=self.session,
                                dt_from=self.dt_from,
                                dt_to=self.dt_to,
                                time_frame=self.time_frame,
                                symbol=self.symbol
                                )
        df_bars = pd.DataFrame(bars, columns=["datetime", "open", "high", "low", "close", "ao", "fisher", "rsi", "mfi"])
        df_bars = df_bars.sort_values("datetime")
        dates = [i.datetime for i in bars]
        x_dates = []
        flags = []
        for i, date in enumerate(dates):
            if i == 0 or date.day != dates[i - 1].day:
                x_dates.append(date.strftime("%d %B %H:%M"))
                flags.append(i)
            else:
                x_dates.append(date.strftime("%H:%M"))
        position = np.arange(len(x_dates))
        locators = [3,4,5]
        locs = []
        for loc in locators:
            for flag in flags[1:]:
                modul = flag % loc
                if not modul:
                    locs.append(loc)
        major_locator = 0
        count = 0
        for loc in locators:
            if locs.count(loc) > count:
                count = locs.count(loc)
                major_locator = loc
        ax_1.set_xticks(position)
        ax_1.set_xticklabels(x_dates, rotation = 45, horizontalalignment = 'left')
        ax_4.set_xticks(position)
        ax_4.set_xticklabels(x_dates, rotation = 45, horizontalalignment = 'right')
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
               labelleft = True,    #  слева
               labelright = False,    #  и справа
                )

        ao = [i.ao for i in bars]
        fisher = [i.fisher for i in bars]
        rsi = [i.rsi for i in bars]
        mfi = [i.mfi for i in bars]
        candlestick2_ohlc(ax=ax_1,
                          opens=df_bars['open'],
                          highs=df_bars['high'],
                          lows=df_bars['low'],
                          closes=df_bars['close'],
                          width=0.6,
                          alpha=1,
                          colordown='red',
                          colorup='green')
        ax_2.bar(np.arange(len(ao)), ao, color="#BA55D3", label="AO")
        ax_3.plot(np.arange(len(fisher)), fisher, color="#DC143C", label="Fish")
        ax_4.plot(np.arange(len(rsi)), rsi, color="#7B68EE", label="RSI")
        ax_4.plot(np.arange(len(rsi)), mfi, color="#FF7F50", label="MFI")

        ax_2.legend()
        ax_3.legend()
        ax_4.legend()

        if entry:
            if type_order == "long":
                arrow = 1
            else:
                arrow = -1
            ax_1.arrow(date_entry, entry - (2*arrow), 0, arrow,
            width = 0.3,
            head_length = 1)
            ax_1.arrow(date_exit, exit + (2*arrow), 0, -arrow,
            width = 0.3,
            head_length = 1)

        plt.subplots_adjust(wspace=0, hspace=0)
        plt.show()


if __name__ == "__main__":
    with get_session() as session:
        graph = Graphs(session, dt_from=datetime.datetime(2022, 4, 1), dt_to=datetime.datetime(2022, 5, 1), time_frame="d1", symbol="AOS")
        graph.create_graph()
