### simple run of prefect flow


1. Within a `web_to_gcs.py`, define a function with a `@flow` decorator.
1. Start prefect server locally (this is a self-hosted approach):
    ```bash
    prefect server start
    ```
1. Define a run a deployment interactively via prefect CLI, the part after colon is the function name that is decorated with `@flow`:
    ```bash
    prefect deploy web_to_gcs.py:web_to_gcs
    ```
    To keep things simple, let name deployment default to `default` and configure most things to run locally.  This means picking up flow code from local (instead of from a remote code repo), starting a local pool of workers (let's name it: `local-process`) and opt-in to save the configuration for this deployment.
1. To execute flow runs from this deployment, start a worker in a separate terminal that pulls work from the `local-process` work pool:
    ```bash
    prefect worker start --pool 'local-process'
    ```
1. To schedule a run for this deployment, use the following command:
    ```bash
    prefect deployment run 'web-to-gcs/default'
    ```

### simple run of GCS (Google Cloud Storage) to GBQ (Google BigQuery)

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
