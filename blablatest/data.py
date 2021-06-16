import pandas as pd
import numpy as np


CURRENCY_PATTERN = r"\((?P<code>\w+)\)"


def extract_exchange_rates(input):
    df = pd.read_csv(
        input,
        sep=";",
        decimal=",",
        na_values="-",
        skiprows=[1, 2, 3, 4, 5],
        parse_dates=[0],
        dayfirst=True,
    )
    currencies = df.columns[1:].str.extract(CURRENCY_PATTERN)["code"]
    df.columns = ["history_date", *currencies.tolist()]
    return df.melt(
        id_vars=["history_date"], var_name="cur_code", value_name="one_euro_value"
    ).dropna()


def extract_serial_codes(input):
    df_meta = pd.read_csv(input, sep=";", nrows=1, index_col=[0])
    currencies = df_meta.columns.str.extract(CURRENCY_PATTERN)["code"]
    df_meta.columns = currencies.tolist()
    df_meta = df_meta.T.rename_axis(["cur_code"], axis=0)
    df_meta.columns = ["serial_code"]
    return df_meta


def compute_pairwise_rates(eur_rates):
    rates_array = np.reshape(eur_rates.values, (-1, 1))
    pairwise_rates = rates_array.T / rates_array
    return (
        pd.DataFrame(
            pairwise_rates,
            index=eur_rates.index.rename("from_cur_code"),
            columns=eur_rates.index.rename("to_cur_code"),
        )
        .stack()
        .to_frame("exchange_rate")
        .query("from_cur_code != to_cur_code")
        .reset_index()
    )
