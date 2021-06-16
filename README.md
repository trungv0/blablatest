# blablatest

Note: this project uses PostgreSQL dialect.
It should also work on Google Cloud SQL Postgres.

## Install dependencies

Dependencies are managed using [poetry](https://python-poetry.org/docs/#installation).

```bash
poetry install
```

## Setup database

Tables must be created before running the main script.

```bash
psql -U [user] [database] < database.sql
```

## Execute

```bash
python -m blablatest [OPTIONS]
```

Options:

* `--postgres-host TEXT`: default `0.0.0.0`
* `--postgres-port INTEGER`: default `5432`
* `--postgres-user TEXT     [required]`
* `--postgres-pass TEXT`: password is NOT recommended to be inputed directly in the script,
  as it will be prompted (as hidden input) on script launch
* `--postgres-db TEXT       [required]`
* `-i, --input TEXT`: url or local path to data file,
  default http://webstat.banque-france.fr/fr/downloadFile.do?id=5385698&exportType=csv

## Unit test

```bash
python -m pytest
```
