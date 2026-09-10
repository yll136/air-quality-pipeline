
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  





with validation_errors as (

    select
        sensor_id, measured_at
    from "awsdatacatalog"."airquality"."stg_measurements"
    group by sensor_id, measured_at
    having count(*) > 1

)

select *
from validation_errors



  
  
      
    ) dbt_internal_test