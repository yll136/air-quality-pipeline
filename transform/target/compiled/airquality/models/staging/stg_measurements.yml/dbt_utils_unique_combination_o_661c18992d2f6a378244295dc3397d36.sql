





with validation_errors as (

    select
        sensor_id, measured_at
    from "awsdatacatalog"."airquality"."stg_measurements"
    group by sensor_id, measured_at
    having count(*) > 1

)

select *
from validation_errors


