from sqlalchemy import Column, String, Integer, ForeignKey, Float, SmallInteger, BigInteger, DateTime, Boolean
from sqlalchemy.orm import relationship
from .db import engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Symbols(Base):

    __tablename__ = "symbols"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)
    group_id = Column(SmallInteger, ForeignKey("groups.id"))
    av_month_vol = Column(Float)
    av_day_vol_last_month = Column(Float)
    av_prof = Column(Float)
    av_prof_last_month = Column(Float)


class Groups(Base):

    __tablename__ = "groups"

    id = Column(SmallInteger, primary_key=True)
    group = Column(String(20), nullable=False)
    symbols = relationship("Symbols")

class Orders(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    date_from = Column(DateTime, nullable=False)
    date_to = Column(DateTime)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), nullable=False)
    typy_order_id = Column(SmallInteger, ForeignKey("type_order.id"), nullable=False)
    profitability = Column(Boolean)
    open = Column(Float, nullable=False)
    close = Column(Float)
    number = Column(Integer, nullable=False)
    stop_loss = Column(Float, nullable=False)
    commission = Column(Float)
    profit = Column(Float)
    symbol = relationship("Symbols", backref="order")



class Type_order(Base):

    __tablename__ = "type_order"

    id = Column(SmallInteger, primary_key=True)
    type = Column(String(10), nullable=False)
    orders = relationship("Orders")


class D1_bars(Base):

    __tablename__ = "d1_bars"

    id = Column(Integer, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    symbol = relationship("Symbols", backref="d1_bar")


class H2_bars(Base):

    __tablename__ = "h2_bars"

    id = Column(BigInteger, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    symbol = relationship("Symbols", backref="h2_bar")


class H1_bars(Base):

    __tablename__ = "h1_bars"

    id = Column(BigInteger, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    symbol = relationship("Symbols", backref="h1_bar")


class M30_bars(Base):

    __tablename__ = "m30_bars"

    id = Column(BigInteger, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    symbol = relationship("Symbols", backref="m30_bar")


class M10_bars(Base):

    __tablename__ = "m10_bars"

    id = Column(BigInteger, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    symbol = relationship("Symbols", backref="m10_bar")


class M5_bars(Base):

    __tablename__ = "m5_bars"

    id = Column(BigInteger, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    symbol = relationship("Symbols", backref="m5_bar")


class M1_bars(Base):

    __tablename__ = "m1_bars"

    id = Column(BigInteger, primary_key=True)
    symbol_id = Column(Integer, ForeignKey("symbols.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    symbol = relationship("Symbols", backref="m1_bar")


# Base.metadata.create_all(engine)
