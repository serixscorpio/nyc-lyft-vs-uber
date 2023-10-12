from prefect.deployments import Deployment, run_deployment

from web_to_gcs import web_to_gcs

if __name__ == "__main__":
    deployment = Deployment.build_from_flow(web_to_gcs, name="web_to_gcs", apply=True, work_pool_name="local-process")
    run_deployment(
        name="web-to-gcs/web_to_gcs",
        parameters={"file_name": "yellow_tripdata_2023-01.parquet"},
    )
    # TODO: follow with another flow 'gcs_to_bq'
