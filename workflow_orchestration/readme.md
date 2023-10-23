## Data Pipeline

![data pipeline](images/nyc_taxi_data_diagram.svg)

## Local Setup
### Prerequisites

- [Install](https://cloud.google.com/sdk/docs/install#deb) `gcloud` CLI.
- Obtain [gcloud credentials](https://cloud.google.com/sdk/gcloud/reference/auth/login): `gcloud auth login`.
- Set current gcloud project ID:`gcloud config set project PROJECT_ID`
- Set up application default credentials: `gcloud auth application-default login`.

### Run pipeline

1. (Optional) Start with a clean slate by [resetting prefect server database](https://docs.prefect.io/2.13.5/guides/host/?h=server#using-the-database):
    ```zsh
    prefect server database reset -y
    ```
1. Start prefect server locally:
    ```bash
    prefect server start
    ```
1. Within a virtual env, start a worker in a separate terminal that pulls work from a work pool named `local-process`:
    ```bash
    prefect worker start --pool 'local-process' --type process
    ```
1. Within a virtual env, start flow run(s):
    ```zsh
    python local_deploy.py
    ```
1. Go to dashboard `http://127.0.0.1:4200/flow-runs` to see flow run(s) in action.