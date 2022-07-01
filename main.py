import MetaTrader5 as mt5
import os
from dotenv import load_dotenv
from pytz import timezone as tz
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from data_base.configuration import CONNECTION_ROW


load_dotenv()

TIME_ZONE = tz('Europe/Moscow')

engine = create_engine(CONNECTION_ROW)
Session = sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    else:
        session.commit()


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
    # mt5.shutdown()
    pass
