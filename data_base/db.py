from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .configuration import CONNECTION_ROW


engine = create_engine(CONNECTION_ROW)
Session = sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
)
session = Session()
