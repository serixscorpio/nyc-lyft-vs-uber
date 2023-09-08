#!/usr/bin/env python
# coding: utf-8

from tempfile import mkdtemp

import click
import psycopg
import pyarrow.dataset as ds
import requests
from pgpq import ArrowToPostgresBinaryEncoder


@click.command()
@click.option("--db", default="ny_taxi")
@click.option("--host", default="pg-database")
@click.option("--port", default=5432)
@click.option(
    "--url",
    default="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-06.parquet",
    help="Source data's URL",
)
@click.option("--user", default="root")
@click.option("--password", default="root")
@click.option("--table_name", default="yellow_taxi_data")
def ingest(
    db: str, host: str, password: str, port: int, table_name: str, url: str, user: str
):
    # let's get some example data
    tmpdir = mkdtemp()
    with open(f"{tmpdir}/input.parquet", mode="wb") as f:
        resp = requests.get(url)
        resp.raise_for_status()
        f.write(resp.content)

    # load an arrow dataset
    dataset = ds.dataset(tmpdir)
    encoder = ArrowToPostgresBinaryEncoder(dataset.schema)
    pg_schema = encoder.schema()
    cols = [
        f'"{col_name}" {col.data_type.ddl()}' for col_name, col in pg_schema.columns
    ]

    ddl_temp = f"CREATE TEMP TABLE data ({','.join(cols)})"
    ddl = f"CREATE TABLE {table_name} ({','.join(cols)})"

    with psycopg.connect(f"postgres://{user}:{password}@{host}:{port}/{db}") as conn:
        with conn.cursor() as cursor:
            cursor.execute(ddl_temp)  # type: ignore
            with cursor.copy("COPY data FROM STDIN WITH (FORMAT BINARY)") as copy:
                copy.write(encoder.write_header())
                for batch in dataset.to_batches():
                    copy.write(encoder.write_batch(batch))
                copy.write(encoder.finish())
            cursor.execute(ddl)  # type: ignore
            cursor.execute(f'INSERT INTO "{table_name}" SELECT * FROM data')


if __name__ == "__main__":
    ingest()
