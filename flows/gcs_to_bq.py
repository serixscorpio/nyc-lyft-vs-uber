from io import BytesIO

import pandas as pd
from google.cloud import bigquery
from prefect import flow
from prefect.deployments import Deployment, run_deployment
from prefect_gcp.cloud_storage import GcsBucket


@flow(name="gcs-to-bq", log_prints=True)
def gcs_to_bq(file_name: str) -> None:
    """
    orchestrate gcs_to_bq
    """
    # input bucket name + gcp credentials (implicit)
    gcs_bucket = GcsBucket(bucket="dtc-tfstate-bucket_evocative-tide-398716")
    # parquet file to panda dataframe
    with BytesIO() as buf:
        gcs_bucket.download_object_to_file_object(file_name, buf)
        df: pd.DataFrame = pd.read_parquet(
            buf,
            columns=[
                "hvfhs_license_num",
                "driver_pay",
                "pickup_datetime",
                "request_datetime",
            ],
        )
    # load dataframe into bigquery
    bigquery.Client().load_table_from_dataframe(
        df,
        "evocative-tide-398716.dtc_nyc_trip_data.rides",
        job_config=bigquery.LoadJobConfig(
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            time_partitioning=bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY,
                field="pickup_datetime",
            ),
            clustering_fields=["hvfhs_license_num"],
        ),
    )


if __name__ == "__main__":
    file_name = "fhvhv_tripdata_2023-07.parquet"
    Deployment.build_from_flow(
        gcs_to_bq, name="gcs_to_bq", apply=True, work_pool_name="local-process"
    )
    run_deployment(
        name="gcs-to-bq/gcs_to_bq",
        parameters={"file_name": file_name},
    )
