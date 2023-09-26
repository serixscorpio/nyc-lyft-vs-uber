from io import BytesIO

import pandas as pd
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
    df.to_gbq(
        destination_table="dtc_nyc_trip_data.rides",
        project_id="evocative-tide-398716",
        if_exists="append",
    )
