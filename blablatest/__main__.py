import click
from blablatest.db import create_connection

import pandas as pd


@click.command()
@click.option("--postgres-host", envvar="POSTGRES_HOST", default="0.0.0.0")
@click.option("--postgres-port", envvar="POSTGRES_PORT", default=5432)
@click.option("--postgres-user", envvar="POSTGRES_USER", required=True)
@click.password_option(
    "--postgres-pass", envvar="POSTGRES_PASS", confirmation_prompt=False
)
@click.option("--postgres-db", envvar="POSTGRES_DB", required=True)
@click.option(
    "-i",
    "--input",
    default="http://webstat.banque-france.fr/fr/downloadFile.do?id=5385698&exportType=csv",
)
def cli(postgres_host, postgres_port, postgres_user, postgres_pass, postgres_db, input):
    with create_connection(
        postgres_host, postgres_port, postgres_user, postgres_pass, postgres_db
    ) as con:
        df = pd.read_sql("select * from dim_currency", con=con)
        print(df.shape)


if __name__ == "__main__":
    cli()
