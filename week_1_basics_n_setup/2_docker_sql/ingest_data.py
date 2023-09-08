#!/usr/bin/env python
# coding: utf-8

from tempfile import mkdtemp

import psycopg
import pyarrow.dataset as ds
import requests
from pgpq import ArrowToPostgresBinaryEncoder

# let's get some example data
tmpdir = mkdtemp()
with open(f"{tmpdir}/input.parquet", mode="wb") as f:
    resp = requests.get(
        "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-06.parquet"
    )
    resp.raise_for_status()
    f.write(resp.content)

# load an arrow dataset
dataset = ds.dataset(tmpdir)
encoder = ArrowToPostgresBinaryEncoder(dataset.schema)
pg_schema = encoder.schema()
cols = [f'"{col_name}" {col.data_type.ddl()}' for col_name, col in pg_schema.columns]

ddl_temp = f"CREATE TEMP TABLE data ({','.join(cols)})"
ddl = f"CREATE TABLE yellow_taxi_data ({','.join(cols)})"

with psycopg.connect("postgres://root:root@pg-database:5432/ny_taxi") as conn:
    with conn.cursor() as cursor:
        cursor.execute(ddl_temp)  # type: ignore
        with cursor.copy("COPY data FROM STDIN WITH (FORMAT BINARY)") as copy:
            copy.write(encoder.write_header())
            for batch in dataset.to_batches():
                copy.write(encoder.write_batch(batch))
            copy.write(encoder.finish())
        cursor.execute(ddl)  # type: ignore
        cursor.execute('INSERT INTO "yellow_taxi_data" SELECT * FROM data')
