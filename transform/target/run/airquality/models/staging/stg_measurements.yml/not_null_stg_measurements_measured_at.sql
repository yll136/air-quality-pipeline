
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select measured_at
from "awsdatacatalog"."airquality"."stg_measurements"
where measured_at is null



  
  
      
    ) dbt_internal_test