from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from configuration import CONNECTION_ROW


engine = create_engine(CONNECTION_ROW)
Session = sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
)

class Data_base():

    @staticmethod
    def save_data_to_db(data):
        with Session() as session:
            try:
                if type(data) == list:
                    session.add_all(data)
                else:
                    session.add(data)
                session.commit()
            except:
                session.rollback()
            print("Saved")

    
