{{ config(materialized="view") }}

select
    timestamp_trunc(pickup_datetime, day) as `date`,
    hvfhs_license_num,
    count(*) as `num_rides`
from {{ ref("stg_rides") }}
group by 1, hvfhs_license_num
