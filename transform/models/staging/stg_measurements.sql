with source as (
    select * from {{ source('raw', 'measurements_raw') }}
),

typed as (
    select
        metro,
        sensor_id,
        location_id,
        location_name,
        lat,
        lon,
        parameter,
        units,
        value,
        cast(from_iso8601_timestamp(hour_utc) as timestamp) as measured_at,
        pct_complete,
        dt
    from source
    where value is not null
      and pct_complete >= 75
),

deduped as (
    select *,
        row_number() over (
            partition by sensor_id, measured_at
            order by pct_complete desc
        ) as rn
    from typed
)

select * from deduped where rn = 1
