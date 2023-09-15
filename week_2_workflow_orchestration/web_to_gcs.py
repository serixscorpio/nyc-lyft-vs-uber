from pathlib import Path

import requests
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket


@task(retries=3, retry_delay_seconds=10)
def fetch_taxi_data() -> Path:
    """
    retrieve parquet file from nyc taxi website, store to local disk
    """
    # set url
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-06.parquet"

    # set local path
    local_path = Path("/tmp/yellow_tripdata_2023-06.parquet")

    # save file to local disk
    with open(local_path, "wb") as f:
        # retrieve file from url
        resp = requests.get(url)
        resp.raise_for_status()
        f.write(resp.content)
    return local_path


@task()
def write_to_gcs(path: Path) -> None:
    """
    upload local file to gcs bucket
    """
    GcsBucket(bucket="dtc-tfstate-bucket_evocative-tide-398716").upload_from_path(
        from_path=path,
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
