
class Data_base():

    @staticmethod
    def save_data_to_db(data, session):
        if type(data) == list:
            session.add_all(data)
        else:
            session.add(data)
