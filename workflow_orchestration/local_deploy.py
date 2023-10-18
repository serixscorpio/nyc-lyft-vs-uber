from prefect.deployments import Deployment, run_deployment

from web_to_bq import web_to_bq

if __name__ == "__main__":
    file_name = "yellow_tripdata_2023-02.parquet"
    Deployment.build_from_flow(web_to_bq, name="web_to_bq", apply=True, work_pool_name="local-process")
    run_deployment(
        name="web-to-bq/web_to_bq",
        parameters={"file_name": file_name},
    )
