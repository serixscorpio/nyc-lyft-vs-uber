"""Create Prefect Blocks"""
import os

from dotenv import load_dotenv
from prefect_dbt.cli import DbtCliProfile
from prefect_dbt.cli.configs import BigQueryTargetConfigs
from prefect_gcp.credentials import GcpCredentials


def save_block(block, name: str = "default") -> None:
    block.save(name, overwrite=True)


def create_blocks() -> None:
    load_dotenv()
    gcp_credentials = GcpCredentials(service_account_file=os.getenv("GCP_SERVICE_ACCOUNT_FILE"))
    save_block(gcp_credentials)

    dbt_cli_profile = DbtCliProfile(
        name="dbt_dwh_models",
        target="default",
        target_configs=BigQueryTargetConfigs(schema=os.getenv("GCP_BIGQUERY_SCHEMA"), credentials=gcp_credentials),
    )
    save_block(dbt_cli_profile)


if __name__ == "__main__":
    create_blocks()
