import logging
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select, func
from contextlib import contextmanager

from blablatest.models import Currency, ExchangeRateHistory

logger = logging.getLogger(__name__)
currency_table = Currency.__table__
history_table = ExchangeRateHistory.__table__


@contextmanager
def create_connection(hostname, port, user, password, database):
    engine = sa.create_engine(
        f"postgresql://{user}:{password}@{hostname}:{port}/{database}"
    )
    with engine.connect() as con:
        yield con


def insert_currency(con, records):
    logger.info("Upsert %d currency entries", len(records))
    insert_stm = insert(currency_table).values(records)
    insert_stm = insert_stm.on_conflict_do_update(
        index_elements=[currency_table.c.cur_code],
        set_=dict(
            one_euro_value=insert_stm.excluded.one_euro_value,
            serial_code=insert_stm.excluded.serial_code,
            last_updated_date=func.current_date(),
        ),
    )
    con.execute(insert_stm)
    logger.info("Upsert done")


def get_last_history_date(con):
    return con.execute(
        select(func.max(history_table.c.history_date))
    ).scalar()


def insert_history(con, records):
    logger.info("Insert %d exchange rate entries", len(records))
    con.execute(history_table.insert(), records)
    logger.info("Insert done")
