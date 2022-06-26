import MetaTrader5 as mt5
import os
from dotenv import load_dotenv
from pytz import timezone as tz
from contextlib import contextmanager


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
    else:
        print("failed to connect at account #{}, error code: {}".format(login, mt5.last_error()))

if __name__=="__main__":
    mt5.shutdown()



# @contextmanager
# def run():
#     try:
#         yield mt5.initialize()
#         login = int(os.environ.get("LOGIN"))
#         password = os.environ.get("PASSWORD")
#         server = os.environ.get("SERVER")
#         authorized = mt5.login(login, password, server)
#         if authorized:
#             print("connected to account #{}".format(login))
#         else:
#             print("failed to connect at account #{}, error code: {}".format(login, mt5.last_error()))
#     except:
#         print("initialize failed")
#         raise
#     else:
#         mt5.shutdown()
    #     login = int(os.environ.get("LOGIN"))
    #     password = os.environ.get("PASSWORD")
    #     server = os.environ.get("SERVER")
    #     authorized = mt5.login(login, password, server)
    #     if authorized:
    #         print("Connected!!!")
    #     else:
    #         print(f"failed to connect at account #{login}, error code: {mt5.last_error()}")
