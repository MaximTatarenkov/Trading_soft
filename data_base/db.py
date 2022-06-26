from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager

from configuration import CONNECTION_ROW


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


class Data_base():

    @staticmethod
    def save_data_to_db(data, session):
        if type(data) == list:
            session.add_all(data)
        else:
            session.add(data)
