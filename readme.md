NYC Lyft vs Uber is a data pipeline I put together to learn data engineering while goign over the curriculum from [DataTalksClub Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp).

I chose to work with well-known data from [NYC Taxi and Limousine Commission (TLC)](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page), specifically focusing on High Volume For-Hire Vehicle Trip Records.  This includes Uber and Lyft trips within NYC (see [data dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_hvfhs.pdf)).  Historically, there are more than two high volume for-hire services in NYC, but Juno and Via ceased operations in November 2019 and December 2021, respectively.

Since this dataset is available to the public, there's probably no paradigm shifting proprietary insight one can glean from it.  But we can point to some evidence when answering trivia questions like:

1. Which day of the week has the most Uber/Lyft trips?
2. On average, does Uber or Lyft have shorter wait times?
3. Do Uber or Lyft drivers get paid more?

## Data Pipeline

![data pipeline](assets/nyc-lyft-vs-uber-pipeline.svg)

## Setup
### Prerequisites

- [Install](https://cloud.google.com/sdk/docs/install#deb) `gcloud` CLI.
- Obtain [gcloud credentials](https://cloud.google.com/sdk/gcloud/reference/auth/login): `gcloud auth login`.
- Set current gcloud project ID:`gcloud config set project PROJECT_ID`
- Set up application default credentials: `gcloud auth application-default login`.
- Run terraform to deploy infrastructure on Google Cloud.

    ```zsh
    terraform init  # initialize terraform
    terraform plan  # build a deployment plan
    terraform apply # apply the deployment plan, actually deploying the infrastructure
    ```

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
1. Within a virtual env, start flow run to load parquet data from GCS into Bigquery:
    ```zsh
    python gcs_to_bq.py
    ```
    - Data is not yet in GCS, download parquet files and then load from GCS into Bigquery:
    ```zsh
    python web_to_bq.py
    ```
1. Go to dashboard `http://127.0.0.1:4200/flow-runs` to see flow run(s) in action.

## Results

This is a dashboard based on the data.

![nyc lyft vs uber dashboard](assets/nyc-lyft-vs-uber-dashboard.gif)

So, which day of the week has the most Uber/Lyft trips?  From the top bar chart, we observe both Uber and Lyft's trip count have a weekly pattern starting with relatively low volumes on Mondays, then steadily increasing mid-week.  Them volumes peak on Saturdays, followed by a drop on Sunday, then back to the trough on Monday.

From the bottom left line graph, we note that Uber drivers get paid more than Lyft drivers on a per trip basis in July 2023.  If I were to become a rideshare driver, I'm more inclined to pick Uber.  Examining the data over a longer time period may strengthen or weaken this claim.  Further causal analysis may be explain the pay difference.

On average, does Uber or Lyft have shorter wait times?  Looking at the bottom right bar chart, Uber trips' wait time distribution tend to skew slightly towards the short end.  However, the difference is probably barely noticeable to a rider since about 80% of Lyft and Uber's trips have wait times under 6 minutes.