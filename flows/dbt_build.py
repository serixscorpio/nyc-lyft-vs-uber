from pathlib import Path

from prefect import flow
from prefect_dbt.cli import DbtCliProfile
from prefect_dbt.cli.commands import trigger_dbt_cli_command


def dbt(command: str = "dbt debug") -> None:
    trigger_dbt_cli_command(
        command=command,
        dbt_cli_profile=DbtCliProfile.load("default"),
        overwrite_profiles=True,
        project_dir=Path(__file__).parent.parent.joinpath("nyc_taxi_dbt").expanduser(),
    )


@flow
def dbt_nyc_lyft_vs_uber(dbt_command: str = "dbt build"):
    dbt(dbt_command)


if __name__ == "__main__":
    dbt_nyc_lyft_vs_uber()
