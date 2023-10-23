{{ config(materialized="view") }}

select cast(max(partition_id) as date format 'YYYYMMDD') as latest_date
from {{ source("nyc_taxi_partition", "PARTITIONS") }}
where table_name = 'rides'
