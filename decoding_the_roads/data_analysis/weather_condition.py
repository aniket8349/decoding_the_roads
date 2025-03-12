from ..utils.sql_utils import create_new_table , execute_query , fetch_query_results


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

        '''
    
        return fetch_query_results(db_config, casualties_query)
        
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


    '''
    
    # Execute the query
    return fetch_query_results(db_config, weather_impact_query)
    
    

