from ..utils.sql_utils import create_new_table , execute_query , fetch_query_results
from ..config.db_config import db_config
from typing import Dict 

from ..config.db_config import db_config

# Most Frequent Causes of Accidents
TABLE_NAME: str = "global_traffic_accidents"
def common_accident_causes(db_config: Dict[str, str]): # to done
    accident_causes_query = f''' 
SELECT 
    `Cause`, 
    COUNT(*) AS `Total_Accidents`, 
    SUM(`Casualties`) AS `Total_Casualties`
FROM `global_traffic_accidents`
WHERE `Cause` IS NOT NULL
GROUP BY `Cause`
ORDER BY `Total_Accidents` DESC;
'''
    return fetch_query_results(db_config, accident_causes_query)
    
def accident_causes_by_casualties(db_config: Dict[str, str]):

    return fetch_query_results(db_config, accident_causes_query)
    
def fetch_all_common_causes(db_config: Dict[str, str]):
    return [common_accident_causes(db_config), accident_causes_by_casualties(db_config)]
    

    
