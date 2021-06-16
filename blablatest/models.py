from sqlalchemy import Column, Float, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Currency(Base):
    __tablename__ = "dim_currency"
    cur_code = Column(String, primary_key=True)
    one_euro_value = Column(Float)
    last_updated_date = Column(Date)
    serial_code = Column(String)


class ExchangeRateHistory(Base):
    __tablename__ = "fact_exchange_rate_history"
    history_date = Column(Date, primary_key=True)
    from_cur_code = Column(
        String, ForeignKey("Currency.cur_code", ondelete="cascade"), primary_key=True
    )
    to_cur_code = Column(
        String, ForeignKey("Currency.cur_code", ondelete="cascade"), primary_key=True
    )
    exchange_rate = Column(Float)
