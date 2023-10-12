## Data Pipeline

![data pipeline](images/nyc_taxi_data_diagram.svg)

## Local Setup
### Prerequisites

- [Install](https://cloud.google.com/sdk/docs/install#deb) `gcloud` CLI.
- Obtain [gcloud credentials](https://cloud.google.com/sdk/gcloud/reference/auth/login): `gcloud auth login`.
- Set current gcloud project ID:`gcloud config set project PROJECT_ID`
- Set up application default credentials: `gcloud auth application-default login`.

### Ingest NYC taxi trip from web to google cloud storage (GCS)

1. (Optional) Start with a clean slate by [resetting prefect server database](https://docs.prefect.io/2.13.5/guides/host/?h=server#using-the-database):
    ```zsh
    prefect server database reset -y
    ```
1. Start prefect server locally:
    ```bash
    prefect server start
    ```
1. Start a worker in a separate terminal that pulls work from a work pool named `local-process`:
    ```bash
    prefect worker start --pool 'local-process' --type process
    ```
1. Start flow run(s):
    ```zsh
    python local_deploy.py
    ```
1. Go to dashboard `http://127.0.0.1:4200/flow-runs` to see flow run(s) in action.

### Load data from GCS (Google Cloud Storage) to GBQ (Google BigQuery)

1. Within `gcs_to_bq.py`, define a function with a `@flow` decorator.
1. Start prefect server locally (this is a self-hosted approach):
    ```bash
    prefect server start
    ```
1. Define a run a deployment interactively via prefect CLI, the part after colon is the function name that is decorated with `@flow`:
    ```bash
    prefect deploy gcs_to_bq.py:gcs_to_bq
    ```
    To keep things simple, let name deployment default to `default` and configure most things to run locally.  This means picking up flow code from local (instead of from a remote code repo), starting a local pool of workers (let's name it: `local-process`) and opt-in to save the configuration for this deployment.
1. To execute flow runs from this deployment, start a worker in a separate terminal that pulls work from the `local-process` work pool:
    ```bash
    prefect worker start --pool 'local-process'
    ```
1. To schedule a run for this deployment, use the following command:
    ```bash
    prefect deployment run 'gcs-to-bq/default'
    ```
