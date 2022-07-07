from sqlalchemy import Column, String, Integer, ForeignKey, Float, SmallInteger, BigInteger, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from main import engine
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base(bind=engine)


class Instruments(Base):

    __tablename__ = "instruments"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), nullable=False)
    name = Column(String(50))
    group_id = Column(SmallInteger, ForeignKey("groups.id"))
    avg_volume = Column(Float)
    avg_volume_lm = Column(Float)
    avg_prof = Column(Float)
    avg_prof_lm = Column(Float)
    atr = Column(Float)
    atr_percent = Column(Float)
    closing_price = Column(Float)
    group = relationship("Groups", backref="instrument")


class Groups(Base):

    __tablename__ = "groups"

    id = Column(SmallInteger, primary_key=True)
    group = Column(String(20), nullable=False)


class Orders(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    date_from = Column(DateTime)
    date_to = Column(DateTime)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    type_order = Column(SmallInteger, ForeignKey("type_order.id"), nullable=False)
    profitability = Column(Boolean)
    open = Column(Float)
    close = Column(Float)
    number = Column(Integer, nullable=False)
    stop_loss = Column(Float, nullable=False)
    commission = Column(Float)
    profit = Column(Float)
    instrument = relationship("Instruments", backref="order")


class StrategyTesting(Base):

    __tablename__ = "strategy_testing"

    id = Column(Integer, primary_key=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    date_from = Column(DateTime)
    date_to = Column(DateTime)
    open = Column(Float)
    close = Column(Float)
    type_order = Column(SmallInteger, ForeignKey("type_order.id"), nullable=False)
    success = Column(Boolean)
    profitability = Column(Float)
    strategy_version = Column(Integer, ForeignKey("type_order.id"), nullable=False)
    instrument = relationship("Instruments", backref="strategy_t")
    strategy = relationship("Strategies", backref="strategy_t")
    t_order = relationship("Type_order", backref="strategy_t")


class Strategies(Base):

    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True)
    strategy = Column(Text, nullable=False)


class Type_order(Base):

    __tablename__ = "type_order"

    id = Column(SmallInteger, primary_key=True)
    type = Column(String(10), nullable=False)
    orders = relationship("Orders")


class D1_bars(Base):

    __tablename__ = "d1_bars"

    id = Column(Integer, primary_key=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    tick_volume = Column(BigInteger)
    real_volume = Column(BigInteger)
    spread = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    instrument = relationship("Instruments", backref="d1_bar")


class H2_bars(Base):

    __tablename__ = "h2_bars"

    id = Column(BigInteger, primary_key=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    tick_volume = Column(BigInteger)
    real_volume = Column(BigInteger)
    spread = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    instrument = relationship("Instruments", backref="h2_bar")


class H1_bars(Base):

    __tablename__ = "h1_bars"

    id = Column(BigInteger, primary_key=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    tick_volume = Column(BigInteger)
    real_volume = Column(BigInteger)
    spread = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    instrument = relationship("Instruments", backref="h1_bar")


class M30_bars(Base):

    __tablename__ = "m30_bars"

    id = Column(BigInteger, primary_key=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    tick_volume = Column(BigInteger)
    real_volume = Column(BigInteger)
    spread = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    instrument = relationship("Instruments", backref="m30_bar")


class M10_bars(Base):

    __tablename__ = "m10_bars"

    id = Column(BigInteger, primary_key=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    tick_volume = Column(BigInteger)
    real_volume = Column(BigInteger)
    spread = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    instrument = relationship("Instruments", backref="m10_bar")


class M5_bars(Base):

    __tablename__ = "m5_bars"

    id = Column(BigInteger, primary_key=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    tick_volume = Column(BigInteger)
    real_volume = Column(BigInteger)
    spread = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    instrument = relationship("Instruments", backref="m5_bar")


class M1_bars(Base):

    __tablename__ = "m1_bars"

    id = Column(BigInteger, primary_key=True)
    instrument_id = Column(Integer, ForeignKey("instruments.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    tick_volume = Column(BigInteger)
    real_volume = Column(BigInteger)
    spread = Column(Integer)
    fisher = Column(Float)
    ao = Column(Float)
    rsi = Column(Float)
    mfi = Column(Float)
    instrument = relationship("Instruments", backref="m1_bar")

if __name__=="__main__":
    print("main")
