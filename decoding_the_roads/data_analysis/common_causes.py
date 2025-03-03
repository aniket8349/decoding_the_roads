from ..utils.sql_utils import create_new_table , execute_query , fetch_query_results
from typing import Dict 

from ..config.db_config import db_config

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
    return fetch_query_results(db_config, accident_causes_query)
    

def accident_causes_by_casualties(db_config: Dict[str, str]):

    accident_casualties_query = f''' 
    SELECT "Cause", SUM("Casualties") AS total_casualties
    FROM `{TABLE_NAME}`
    GROUP BY "Cause"
    ORDER BY total_casualties DESC
    LIMIT 10;
    '''
    
    return fetch_query_results(db_config, accident_casualties_query)
    
def fetch_all_common_causes(db_config: Dict[str, str]):
    return [common_accident_causes(db_config), accident_causes_by_casualties(db_config)]
    
if __name__ == "__main__":
    print(fetch_all_common_causes(db_config))  