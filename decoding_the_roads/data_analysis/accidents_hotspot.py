from ..utils.sql_utils import create_new_table , execute_query , fetch_query_results
from ..config.db_config import db_config
from typing import Dict 

from ..config.db_config import db_config

#Identifying Most Accident-Prone Locations 
TABLE_NAME: str = "global_traffic_accidents"
def accident_hotspots_by_weather(db_config: Dict[str, str]):
    accident_hotspot_query = f''' 
    SELECT 
    `Location`, 
    `Weather Condition`, 
    COUNT(*) AS `Total_Accidents`, 
    SUM(`Casualties`) AS `Total_Casualties`
FROM `global_traffic_accidents`
WHERE `Location` IS NOT NULL AND `Weather Condition` IS NOT NULL
GROUP BY `Location`, `Weather Condition`
ORDER BY `Total_Accidents` DESC
LIMIT 10;

    '''
    
    # Execute the query
    return fetch_query_results(db_config, accident_hotspot_query)
    
    # Print the results

    


def accident_hotspots_by_month(db_config: Dict[str, str]):
    
    accident_hotspot_query = f''' 
    SELECT 
    `Location`, 
    DATE_FORMAT(`Date`, '%b') AS `Month`, 
    COUNT(*) AS `Total_Accidents`, 
    SUM(`Casualties`) AS `Total_Casualties`
FROM `global_traffic_accidents`
WHERE `Location` IS NOT NULL AND `Date` IS NOT NULL
GROUP BY `Location`, `Month`
ORDER BY `Total_Accidents` DESC
LIMIT 10;

    '''
    
    return fetch_query_results(db_config, accident_hotspot_query)
    
    
def fetch_all_accident_hotspots(db_config: Dict[str, str]):
    return [accident_hotspots_by_weather(db_config), accident_hotspots_by_month(db_config)]
    
if __name__ == "__main__":
    # accident_hotspots_by_month(db_config)
    print(fetch_all_accident_hotspots(db_config))

    
""" 
[[('Location', 'Weather Condition', 1024)], [('Location', 'Month', 1024)]] ?
# accident_hotspots_by_month
[('Location', 'Weather Condition', 1024)]
[('Mumbai, India', 'Snow' , 123)]

"""
    

