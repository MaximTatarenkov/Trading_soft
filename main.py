import MetaTrader5 as mt5
import os
from dotenv import load_dotenv
from datetime import datetime
from pytz import timezone as tz

from rates.indicators import Indicator
from rates.bars import Rates

load_dotenv()

TIME_ZONE = tz('Europe/Moscow')

def run():
    if not mt5.initialize():
        print("initialize failed")
        mt5.shutdown()
    login = int(os.environ.get("LOGIN"))
    password = os.environ.get("PASSWORD")
    server = os.environ.get("SERVER")
    authorized = mt5.login(login, password, server)
    if authorized:
        print("Connected!!!")
        # currentTimeZone = tz('Europe/Moscow')
        # date_from = datetime(2011, 9, 30, tzinfo=currentTimeZone)
        # rates = Rates(symbol="BTCUSD", time_frame="m5", bars_count=50, date_from=date_from)
        # bars = rates.get_bars_from()
        # print(bars)
        # indicator = Indicator(bars)
        # bars_and_indicators = indicator.attach_indicators()
    else:
        print("failed to connect at account #{}, error code: {}".format(login, mt5.last_error()))


mt5.shutdown()
