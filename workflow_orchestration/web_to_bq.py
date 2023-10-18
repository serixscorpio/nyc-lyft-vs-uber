from prefect import flow

from gcs_to_bq import gcs_to_bq
from web_to_gcs import web_to_gcs


@flow(name="web-to-bq", log_prints=True)
def web_to_bq(file_name: str) -> None:
    web_to_gcs(file_name)
    gcs_to_bq(file_name)
