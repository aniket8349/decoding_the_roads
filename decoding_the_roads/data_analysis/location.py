from ..utils.sql_utils import create_new_table , execute_query , fetch_query_results
from ..config.db_config import db_config
from typing import Dict 

TABLE_NAME: str = "global_traffic_accidents"

def location_cause_casualties(db_config: Dict[str, str]):
    monthly_impact_query = f''' 
    SELECT 
    `Location`, 
    `Cause`, 
    SUM(`Casualties`) AS `Total_Casualties`
FROM `global_traffic_accidents`
WHERE `Location` IS NOT NULL AND `Cause` IS NOT NULL
GROUP BY `Location`, `Cause`
ORDER BY `Total_Casualties` DESC;


    '''
    
    # Execute the query
    return fetch_query_results(db_config, monthly_impact_query)

def casualties_by_location_weather(db_config: Dict[str, str]):
    query = f''' 
    SELECT 
        `Location`, 
        `Weather Condition`, 
        SUM(`Casualties`) AS `Total_Casualties`
    FROM `global_traffic_accidents`
    WHERE `Location` IS NOT NULL AND `Weather Condition` IS NOT NULL
    GROUP BY `Location`, `Weather Condition`
    ORDER BY `Total_Casualties` DESC
    LIMIT 10;
    '''
    
    # Execute the query
    return fetch_query_results(db_config, query)


def casualties_by_location_road_condition(db_config: Dict[str, str]):
    query = f''' 
    SELECT 
    `Location`, 
    `Road Condition`, 
    SUM(`Casualties`) AS `Total_Casualties`
FROM `global_traffic_accidents`
WHERE `Location` IS NOT NULL AND `Road Condition` IS NOT NULL
GROUP BY `Location`, `Road Condition`
ORDER BY `Total_Casualties` DESC
LIMIT 10;

    '''
    
    # Execute the query
    return fetch_query_results(db_config, query)



if __name__ == "__main__":
    result = casualties_by_location_road_condition(db_config)
    print(result)
    