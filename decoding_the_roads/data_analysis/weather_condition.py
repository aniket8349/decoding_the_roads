from ..utils.sql_utils import create_new_table , execute_query , fetch_query_results
<<<<<<< HEAD
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
=======
from ..config.db_config import db_config
from typing import Dict 



# quiries for selecting weather condition and casualties 
TABLE_NAME: str = "global_traffic_accidents"
def weather_condition_casualties(db_config:Dict[str,str]):# to done
    
    weather_condition_quaries = f''' 
    SELECT 
    `Weather Condition`, 
    COUNT(*) AS `Total_Accidents`, 
    SUM(`Casualties`) AS `Total_Casualties`
FROM `global_traffic_accidents`
WHERE `Weather Condition` IS NOT NULL
GROUP BY `Weather Condition`
ORDER BY `Total_Casualties` DESC;

    '''
    return fetch_query_results(db_config, weather_condition_quaries)
    

#-------------------------------------------------------------------   
def accident_count_per_weather(db_config: Dict[str, str]): #to done
        
        accident_count_query = f''' 
SELECT 
    `Weather Condition`, 
    COUNT(*) AS `Total_Accidents`
FROM `global_traffic_accidents`
WHERE `Weather Condition` IS NOT NULL
GROUP BY `Weather Condition`
ORDER BY `Total_Accidents` DESC;

    '''
        return fetch_query_results(db_config, accident_count_query)
        
#---------------------------------------------  
    
def monthly_casualties_per_weather(db_config: Dict[str, str]): # to change for month 2023 and 2024 (specifie weather)
        casualties_query = f''' 
        SELECT 
    DATE_FORMAT(`Date`, '%b') AS `Month`,  
    `Weather Condition`, 
    SUM(`Casualties`) AS `Total_Casualties`
FROM `global_traffic_accidents`
WHERE `Date` IS NOT NULL AND `Weather Condition` IS NOT NULL
GROUP BY `Month`, `Weather Condition`
ORDER BY STR_TO_DATE(`Month`, '%b'), `Total_Casualties` DESC;

>>>>>>> origin/bug-analysis-system
        '''
    
        return fetch_query_results(db_config, casualties_query)
        
<<<<<<< HEAD
    

def accidents_and_casualties_by_weather(db_config: Dict[str, str]):  #accident count and total casualties for each weather condition:
    
    weather_impact_query = f''' 
    SELECT 
        "Weather Condition", 
        COUNT(*) AS accident_count, 
        SUM("Casualties") AS total_casualties
    FROM `{TABLE_NAME}`
    GROUP BY "Weather Condition"
    ORDER BY total_casualties DESC;
=======
#------------------------------------------------- 

def accidents_and_casualties_by_weather(db_config: Dict[str, str]): 
    #accident count and total casualties for each weather condition: (to done)

    weather_impact_query = f''' 
    SELECT 
    `Weather Condition`, 
    COUNT(*) AS `Total_Accidents`, 
    SUM(`Casualties`) AS `Total_Casualties`
FROM `global_traffic_accidents`
WHERE `Weather Condition` IS NOT NULL
GROUP BY `Weather Condition`
ORDER BY `Total_Casualties` DESC;

>>>>>>> origin/bug-analysis-system
    '''
    
    # Execute the query
    return fetch_query_results(db_config, weather_impact_query)
    
    
<<<<<<< HEAD

def fetch_all_weather_conditions(db_config: Dict[str, str]):
    # result = [accidents_and_casualties_by_weather(db_config),accident_count_per_weather(db_config),highest_casualties_weather(db_config),monthly_casualties_per_weather(db_config)]
    result = accidents_and_casualties_by_weather(db_config)
    return result



if __name__ == "__main__":
    print(fetch_all_weather_conditions(db_config))
=======
if __name__ == "__main__":
    result =weather_condition_casualties(db_config)
    print(result)
>>>>>>> origin/bug-analysis-system
    