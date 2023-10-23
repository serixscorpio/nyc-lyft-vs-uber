{{ config(materialized="table") }}

{% set sql_latest_date %}
    select latest_date from {{ ref("stg_latest_date") }}
{% endset %}

select *
from {{ source("nyc_taxi", "rides") }}
{% if target.name == "dev" %}
    -- limit data size to the latest partition (latest date) when working in dev.
    where
        timestamp_trunc(pickup_datetime, day)
        = timestamp('{{ dbt_utils.get_single_value(sql_latest_date) }}')
{% endif %}
