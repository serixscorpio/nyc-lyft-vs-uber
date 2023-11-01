import os

from dotenv import load_dotenv
from prefect_gcp.credentials import GcpCredentials

load_dotenv()


def save_block(block, name: str = "default") -> None:
    block.save(name, overwrite=True)


gcp_credentials = GcpCredentials(service_account_file=os.getenv("GCP_SERVICE_ACCOUNT_FILE"))
save_block(gcp_credentials)
