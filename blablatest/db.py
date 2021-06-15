import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from contextlib import contextmanager

from blablatest.models import Currency, ExchangeRateHistory

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
    insert_stm = insert(currency_table).values(records)
    insert_stm = insert_stm.on_conflict_do_update(
        index_elements=[currency_table.c.cur_code],
        set_=dict(
            one_euro_value=insert_stm.excluded.one_euro_value,
            serial_code=insert_stm.excluded.serial_code,
            last_updated_date=sa.text("current_date"),
        ),
    )
    con.execute(insert_stm)
