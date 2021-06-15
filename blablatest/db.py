import sqlalchemy as sa
from contextlib import contextmanager


@contextmanager
def create_connection(hostname, port, user, password, database):
    engine = sa.create_engine(
        f"postgresql://{user}:{password}@{hostname}:{port}/{database}"
    )
    with engine.connect() as con:
        yield con
