from prefect import flow
from prefect.deployments import Deployment, run_deployment

from gcs_to_bq import gcs_to_bq
from web_to_gcs import web_to_gcs


@flow(name="web-to-bq", log_prints=True)
def web_to_bq(file_name: str) -> None:
    web_to_gcs(file_name)
    gcs_to_bq(file_name)


if __name__ == "__main__":
    file_name = "fhvhv_tripdata_2023-07.parquet"
    Deployment.build_from_flow(
        web_to_bq, name="web_to_bq", apply=True, work_pool_name="local-process"
    )
    run_deployment(
        name="web-to-bq/web_to_bq",
        parameters={"file_name": file_name},
    )
