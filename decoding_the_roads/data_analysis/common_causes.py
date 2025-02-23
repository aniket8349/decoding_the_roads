from ..utils.sql_utils import create_new_table , execute_query , fetch_query_results
from typing import Dict 



# Most Frequent Causes of Accidents
TABLE_NAME: str = "global_traffic_accidents"
def common_accident_causes(db_config: Dict[str, str]):
    accident_causes_query = f''' 
    SELECT "Cause", COUNT(*) AS accident_count
    FROM `{TABLE_NAME}`
    GROUP BY "Cause"
    ORDER BY accident_count DESC
    LIMIT 10;
    '''
    result = fetch_query_results(db_config, accident_causes_query)
    print(result)

def accident_causes_by_casualties(db_config: Dict[str, str]):

    accident_casualties_query = f''' 
    SELECT "Cause", SUM("Casualties") AS total_casualties
    FROM `{TABLE_NAME}`
    GROUP BY "Cause"
    ORDER BY total_casualties DESC
    LIMIT 10;
    '''
    
    result = fetch_query_results(db_config, accident_casualties_query)
    
    
    print(result)
