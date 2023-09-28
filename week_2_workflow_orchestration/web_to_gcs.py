from pathlib import Path

from io import BytesIO
import requests
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3, retry_delay_seconds=10)
def fetch_taxi_data() -> BytesIO:
    """
    retrieve parquet file from nyc taxi website, store to local disk
    """
    # set url
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-06.parquet"

    # retrieve file content from url
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.content


@task()
def write_to_gcs(path: Path) -> None:
    """
    upload local file to gcs bucket
    """
    GcsBucket(
        bucket="dtc-tfstate-bucket_evocative-tide-398716"
    ).upload_from_file_object(
        from_file_object=binary_io,
    )
    return


@flow(name="web-to-gcs", log_prints=True)
def web_to_gcs() -> None:
    """
    orchestrate web_to_gcs
    """
    path = fetch_taxi_data()
    write_to_gcs(path)
    return


# trigger cloud function to load data into bigquery (tentative)
