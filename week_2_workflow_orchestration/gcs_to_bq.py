from io import BytesIO

import pandas as pd
from google.cloud import bigquery
from prefect import flow
from prefect_gcp.cloud_storage import GcsBucket


@flow(name="gcs-to-bq", log_prints=True)
def gcs_to_bq():
    """
    orchestrate gcs_to_bq
    """
    # input bucket name + gcp credentials (implicit)
    gcs_bucket = GcsBucket(bucket="dtc-tfstate-bucket_evocative-tide-398716")
    with BytesIO() as buf:
        gcs_bucket.download_object_to_file_object(
            "yellow_tripdata_2023-06.parquet", buf
        )
        df: pd.DataFrame = pd.read_parquet(buf)
    # parquet file to panda dataframe
    # fill in zero passengers
    print(f"pre: missing passenger count: {df.passenger_count.isna().sum()}")
    df.passenger_count.fillna(0, inplace=True)
    print(f"post: missing passenger count: {df.passenger_count.isna().sum()}")
    # 3. panda dataframe to bigquery
    # approach 2: use bigquery client
    bigquery.Client().load_table_from_dataframe(
        df,
        "evocative-tide-398716.dtc_nyc_trip_data.rides",
        job_config=bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",
            time_partitioning=bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="tpep_pickup_datetime",
            ),
            # range_partitioning=bigquery.table.RangePartitioning(
            #     field="payment_type",
            #     range_=bigquery.table.PartitionRange(start=1, end=7, interval=1),
            # ),
            # clustering_fields=["tpep_pickup_datetime"],
            clustering_fields=["payment_type"],
        ),
    )
    # approach 1: use pandas-gbq
    # df.to_gbq(
    #     destination_table="dtc_nyc_trip_data.rides",
    #     project_id="evocative-tide-398716",
    #     if_exists="append",
    # )
