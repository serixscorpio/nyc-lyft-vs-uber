{{ config(materialized="view", cluster_by=["pickup_datehour", "hvfhs_company"]) }}

select
    case when hvfhs_license_num = 'HV0003' then 'Uber'
         when hvfhs_license_num = 'HV0005' then 'Lyft'
         else 'Other'
    end as hvfhs_company,
    driver_pay,
    timestamp_trunc(pickup_datetime, hour) as pickup_datehour
    -- timestamp_diff(pickup_datetime, request_datetime, MINUTE) as wait_time_in_minutes
from {{ source("nyc_taxi", "rides") }}
where driver_pay > 0
