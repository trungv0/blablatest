# blablatest

Note: this project uses PostgreSQL dialect.
It should also work on Google Cloud SQL Postgres.

## Install dependencies

Dependencies are managed using [poetry](https://python-poetry.org/docs/#installation).

```bash
poetry install
```

## Execute

```bash
python -m blablatest [OPTIONS]
```

Options:

* `--postgres-host TEXT`
* `--postgres-port INTEGER`
* `--postgres-user TEXT     [required]`
* `--postgres-pass TEXT`
* `--postgres-db TEXT       [required]`
* `-i, --input TEXT`

## Unit test

```bash
python -m pytest
```
