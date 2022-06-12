import MetaTrader5 as mt5
# import pandas as pd
import os
from datetime import datetime
from finta import TA
from dotenv import load_dotenv

from indicators import Indicator

load_dotenv()

if not mt5.initialize():
    print("initialize failed")
    mt5.shutdown()


login = int(os.environ.get("LOGIN"))
password = os.environ.get("PASSWORD")
server = os.environ.get("SERVER")
authorized = mt5.login(login, password, server)
if authorized:
    symbol = mt5.symbol_info_tick("BTCUSD")
    date_sec = symbol._asdict()["time"]
    date = datetime.fromtimestamp(date_sec)
    indicator = Indicator("BTCUSD", 100, "1h")
    fish = indicator.get_fisher()
    # nm_arr = mt5.copy_rates_from_pos("BTCUSD", mt5.TIMEFRAME_M30, 0, 100)
    # data_frame = pd.DataFrame(nm_arr, columns=["time", "open", "high", "low", "close", "tick_volume", "spread", "real_volume"])
    # data_frame["time"] = pd.to_datetime(data_frame["time"], unit="s")
    # data_frame.rename(columns = {'tick_volume' : 'volume'}, inplace = True)
    # changed_data_frame = data_frame.drop(["spread", "real_volume"], axis=1)
    # fish = TA.FISH(changed_data_frame, 10)
    # ao = TA.AO(changed_data_frame)
    # aoc = {}
    # for i, v in enumerate(ao):
    #     aoc[f'{len(ao) - i}'] = v
    print(fish)
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

# завершим подключение к терминалу MetaTrader 5
mt5.shutdown()
