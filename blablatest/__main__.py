import click
from blablatest.db import create_connection, insert_currency, insert_history, get_last_history_date
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

        last_values = (
            df.sort_values("history_date", ascending=False)
            .drop_duplicates("cur_code")
            .drop("history_date", axis=1)
            .merge(df_meta, on="cur_code")
        )
        if len(last_values) > 0:
            insert_currency(con, last_values.to_dict("records"))
        last_date = get_last_history_date(con)

        # skip processed dates to avoid redundant computation
        if last_date is not None:
            df = df.query("history_date > @last_date")

        if len(df) > 0:
            # compute pairwise rates for each date
            df_rates = pd.concat(
                [
                    compute_pairwise_rates(subdf.set_index("cur_code")["one_euro_value"]).assign(
                        history_date=history_date
                    )
                    for history_date, subdf in df.groupby("history_date")
                ]
            )
            if len(df_rates) > 0:
                insert_history(con, df_rates.to_dict("records"))


if __name__ == "__main__":
    cli()
