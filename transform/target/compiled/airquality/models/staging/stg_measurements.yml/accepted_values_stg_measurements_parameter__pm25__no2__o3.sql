
    
    

with all_values as (

    select
        parameter as value_field,
        count(*) as n_records

    from "awsdatacatalog"."airquality"."stg_measurements"
    group by parameter

)

select *
from all_values
where value_field not in (
    'pm25','no2','o3'
)


