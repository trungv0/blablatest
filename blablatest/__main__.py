import click
from blablatest.db import create_connection
from blablatest.data import (
    extract_exchange_rates,
    extract_serial_codes,
    compute_pairwise_rates,
)
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
        df = extract_exchange_rates(input)
        df_meta = extract_serial_codes(input)

        # compute pairwise rates for each date
        # TODO skip dates that existed in the DB
        df_rates = pd.concat(
            [
                compute_pairwise_rates(subdf.set_index("cur_code")["rate"]).assign(
                    history_date=history_date
                )
                for history_date, subdf in df.groupby("history_date")
            ]
        )

        print(df.shape)


if __name__ == "__main__":
    cli()
