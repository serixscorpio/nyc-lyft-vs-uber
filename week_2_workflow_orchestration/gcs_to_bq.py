import pandas as pd
from prefect import flow
from prefect_gcp.cloud_storage import GcsBucket


@flow(name="gcs-to-bq", log_prints=True)
def gcs_to_bq():
    """
    orchestrate gcs_to_bq
    """
    # input bucket name + gcp credentials (implicit)
    gcs_path = GcsBucket(
        bucket="dtc-tfstate-bucket_evocative-tide-398716"
    ).download_object_to_path("yellow_tripdata_2023-06.parquet")
    # parquet file to panda dataframe
    df = pd.read_parquet(gcs_path)
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
