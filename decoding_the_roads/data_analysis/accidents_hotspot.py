from ..utils.sql_utils import create_new_table , execute_query , fetch_query_results
from ..config.db_config import db_config
from typing import Dict 

from ..config.db_config import db_config

#Identifying Most Accident-Prone Locations 
TABLE_NAME: str = "global_traffic_accidents"
def accident_hotspots_by_weather(db_config: Dict[str, str]):
    accident_hotspot_query = f''' 
    SELECT "Location", "Weather Condition", COUNT(*) AS accident_count
    FROM `{TABLE_NAME}`
    GROUP BY "Location", "Weather Condition"
    ORDER BY accident_count DESC
    LIMIT 20;
    '''
    
    # Execute the query
    return fetch_query_results(db_config, accident_hotspot_query)
    
    # Print the results
     
    


def accident_hotspots_by_month(db_config: Dict[str, str]):
    
    accident_hotspot_query = f''' 
    SELECT "Location", "Month", COUNT(*) AS accident_count
    FROM `{TABLE_NAME}`
    GROUP BY "Location", "Month"
    ORDER BY accident_count DESC
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
    

