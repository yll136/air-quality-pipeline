{{ config(materialized='table') }}

with pm25 as (
    select metro, location_name, measured_at, value as pm25_ugm3
    from {{ ref('stg_measurements') }}
    where parameter = 'pm25'
),

weather as (
    select metro, measured_at, temp_c, wind_kmh, humidity_pct
    from {{ ref('stg_weather') }}
)

select
    p.metro,
    p.location_name,
    p.measured_at,
    p.pm25_ugm3,
    w.temp_c,
    w.wind_kmh,
    w.humidity_pct,
    p.pm25_ugm3 > 15 as over_who_daily
from pm25 p
left join weather w
    on  p.metro = w.metro
    and p.measured_at = w.measured_at
-- ci smoke test
