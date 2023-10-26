/*
For each company, tally the number of rides and percentage of rides that have wait times
of 0~1 minute, 1~2 minutes, 2~3 minutes, ..., 15~16 minutes.
This helps answer questions like "What percentage of Lyft rides have wait times of 5 minute or less?"
 */
{{ config(materialized="table") }}

select
    hvfhs_company,
    wait_time_in_minutes,
    count(*) as `number_of_rides`,
    count(*)
    * 100
    / sum(count(*)) over (partition by hvfhs_company) as `percentage_of_rides`
from {{ ref("stg_rides") }}
where wait_time_in_minutes between 0 and 15
group by hvfhs_company, wait_time_in_minutes
