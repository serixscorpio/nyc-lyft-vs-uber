"""Deploy flows locally"""
from prefect.deployments import Deployment

from create_blocks import create_blocks
from flows import dbt_build, gcs_to_bq, web_to_gcs

if __name__ == "__main__":
    create_blocks()
    Deployment.build_from_flow(web_to_gcs.web_to_gcs, name="local-process", apply=True)
    Deployment.build_from_flow(gcs_to_bq.gcs_to_bq, name="local-process", apply=True)
    Deployment.build_from_flow(dbt_build.dbt_nyc_lyft_vs_uber, name="local-process", apply=True)
