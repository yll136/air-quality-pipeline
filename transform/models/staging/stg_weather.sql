with source as (
    select * from {{ source('raw', 'weather_raw') }}
),

typed as (
    select
        metro,
        date_parse(hour_utc, '%Y-%m-%dT%H:%i') as measured_at,
        temp_c,
        wind_kmh,
        humidity_pct
    from source
    where temp_c is not null
),

deduped as (
    select *,
        row_number() over (
            partition by metro, measured_at
            order by measured_at
        ) as rn
    from typed
)

select metro, measured_at, temp_c, wind_kmh, humidity_pct
from deduped where rn = 1
