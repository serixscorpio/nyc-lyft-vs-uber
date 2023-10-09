from io import BytesIO

import httpx
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3, retry_delay_seconds=10)
def fetch_taxi_data(from_path_name: str) -> BytesIO:
    """
    retrieve parquet file from nyc taxi website
    """
    # set url
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{from_path_name}"

    # retrieve file content from url
    resp = httpx.get(url)
    resp.raise_for_status()
    return BytesIO(resp.content)


@task()
def write_to_gcs(b: BytesIO, to_path_name: str) -> None:
    """
    upload local file to gcs bucket
    """
    GcsBucket(
        bucket="dtc-tfstate-bucket_evocative-tide-398716"
    ).upload_from_file_object(from_file_object=b, to_path=to_path_name, timeout=600)
    return


@flow(name="web-to-gcs", log_prints=True)
def web_to_gcs(file_name: str = "yellow_tripdata_2023-06.parquet") -> None:
    """
    orchestrate web_to_gcs
    """
    b = fetch_taxi_data(file_name)
    write_to_gcs(b, file_name)
    return


# trigger cloud function to load data into bigquery (tentative)
