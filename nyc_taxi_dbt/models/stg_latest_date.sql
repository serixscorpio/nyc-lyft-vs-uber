-- This is a materialized view to determine the latest date
{{ config(materialized="view") }}

select cast(max(partition_id) as date format 'YYYYMMDD') as latest_date
from {{ source("warehouse_partition", "PARTITIONS") }}
where table_name = 'rides'