import pandas as pd

import data_base.models as models

TIME_FRAME_TABLES = {"d1": models.D1_bars,
                     "h2": models.H2_bars,
                     "h1": models.H1_bars,
                     "m30": models.M30_bars,
                     "m10": models.M10_bars,
                     "m5": models.M5_bars,
                     "m1": models.M1_bars,
                     }

class Data_base():

    @staticmethod
    def save_data_to_db(data, session):
        if type(data) == list:
            session.add_all(data)
        else:
            session.add(data)

    @staticmethod
    def get_bars_from_db_with_date(session, dt_from, dt_to, symbol, time_frame):
        table = TIME_FRAME_TABLES[time_frame]
        instrument_id = session.query(models.Instruments.id).filter(models.Instruments.symbol==symbol).one()[0]
        data = session.query(
            table.id,
            table.datetime,
            table.open,
            table.high,
            table.low,
            table.close,
            table.ao,
            table.fisher,
            table.rsi,
            table.mfi).filter(table.instrument_id==instrument_id, dt_from <= table.datetime, table.datetime <= dt_to).order_by(table.datetime).all()
        return data

    @staticmethod
    def get_bars_from_db_all(session, symbol, time_frame):
        table = TIME_FRAME_TABLES[time_frame]
        instrument_id = session.query(models.Instruments.id).filter(models.Instruments.symbol==symbol).one()[0]
        data = session.query(
            table.id,
            table.datetime,
            table.open,
            table.high,
            table.low,
            table.close,
            table.real_volume,
            table.ao,
            table.fisher,
            table.rsi,
            table.mfi).filter(table.instrument_id==instrument_id).order_by(table.datetime).all()
        df_data = pd.DataFrame(data, columns=["id", "datetime", "open", "high", "low", "close", "volume", "ao", "fisher", "rsi", "mfi"])
        return df_data

    @staticmethod
    def get_2bars_using_date(session, symbol, time_frame, datetime):
        table = TIME_FRAME_TABLES[time_frame]
        instrument_id = session.query(models.Instruments.id).filter(models.Instruments.symbol==symbol).one()[0]
        data = session.query(
            table.id,
            table.datetime,
            table.open,
            table.high,
            table.low,
            table.close,
            table.real_volume,
            table.ao,
            table.fisher,
            table.rsi,
            table.mfi).order_by(table.datetime.desc()).filter(table.instrument_id==instrument_id, table.datetime<datetime).limit(2)
        # prev_image = session.query(Images).order_by(Images.id.desc()).filter(Images.id < id).limit(2)
        df_data = pd.DataFrame(data, columns=["id", "datetime", "open", "high", "low", "close", "volume", "ao", "fisher", "rsi", "mfi"])
        return df_data

if __name__=="__main__":
    print("main")
