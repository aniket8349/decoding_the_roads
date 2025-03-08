from ..utils.sql_utils import create_new_table , execute_query , fetch_query_results
from typing import Dict 

from ..config.db_config import db_config

# quiries for selecting weather condition and casualties 
TABLE_NAME: str = "global_traffic_accidents"
def weather_condition_casualties(db_config:Dict[str,str]):
    
    weather_condition_quaries = f''' 
    select "Weather Condition", "Casualties" from `{TABLE_NAME}`;
    '''
    return fetch_query_results(db_config, weather_condition_quaries)
    
    
def highest_casualties_weather(db_config: Dict[str, str]):
        casualties_query = f''' 
        SELECT "Weather Condition", SUM("Casualties") AS total_casualties
        FROM `{TABLE_NAME}`
        GROUP BY "Weather Condition"
        ORDER BY total_casualties DESC;
        '''
    
        return fetch_query_results(db_config, casualties_query)
        
    
def accident_count_per_weather(db_config: Dict[str, str]):
        
        accident_count_query = f''' 
        SELECT "Weather Condition", COUNT(*) AS accident_count
        FROM `{TABLE_NAME}`
        GROUP BY "Weather Condition"
        ORDER BY accident_count DESC;
    '''
        return fetch_query_results(db_config, accident_count_query)
        
    
    
def monthly_casualties_per_weather(db_config: Dict[str, str]): 
        casualties_query = f''' 
        SELECT "Weather Condition", "Month", SUM("Casualties") AS total_casualties
        FROM `{TABLE_NAME}`
        GROUP BY "Weather Condition", "Month"
        ORDER BY "Month", total_casualties DESC;
        '''
    
        return fetch_query_results(db_config, casualties_query)
        
    

def accidents_and_casualties_by_weather(db_config: Dict[str, str]):  #accident count and total casualties for each weather condition:
    
    weather_impact_query = f''' 
    SELECT 
        "Weather Condition", 
        COUNT(*) AS accident_count, 
        SUM("Casualties") AS total_casualties
    FROM `{TABLE_NAME}`
    GROUP BY "Weather Condition"
    ORDER BY total_casualties DESC;
    '''
    
    # Execute the query
    return fetch_query_results(db_config, weather_impact_query)
    
    

def fetch_all_weather_conditions(db_config: Dict[str, str]):
    # result = [accidents_and_casualties_by_weather(db_config),accident_count_per_weather(db_config),highest_casualties_weather(db_config),monthly_casualties_per_weather(db_config)]
    result = accidents_and_casualties_by_weather(db_config)
    return result



if __name__ == "__main__":
    print(fetch_all_weather_conditions(db_config))
    