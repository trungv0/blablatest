create table dim_currency (
    cur_code varchar primary key,
    one_euro_value float,
    last_updated_date timestamptz default current_timestamp,
    serial_code varchar
);

create table fact_exchange_rate_history (
    history_date date,
    from_cur_code varchar references dim_currency(cur_code),
    to_cur_code varchar references dim_currency(cur_code),
    exchange_rate float,
    primary key (history_date, from_cur_code, to_cur_code)
);
