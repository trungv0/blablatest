create table dim_currency (
    cur_code varchar primary key,
    one_euro_value float,
    last_updated_date date default current_date,
    serial_code varchar
);

create table fact_exchange_rate_history (
    history_date date,
    from_cur_code varchar references dim_currency(cur_code) on delete cascade,
    to_cur_code varchar references dim_currency(cur_code) on delete cascade,
    exchange_rate float,
    primary key (history_date, from_cur_code, to_cur_code)
);
