from ..utils.sql_utils import create_new_table , execute_query , fetch_query_results
from ..config.db_config import db_config
from typing import Dict 



#Identifying the year and month of most accidents count and causalties 
TABLE_NAME: str = "global_traffic_accidents"

def accidents_and_casualties_by_month(db_config: Dict[str, str]):#accidents_and_casualties_by_month
    monthly_impact_query = f''' 
    SELECT DATE_FORMAT(Date, '%b') AS Month, COUNT(*) AS Total_Accidents, SUM(Casualties) AS Total_Casualties
FROM `{TABLE_NAME}`
GROUP BY DATE_FORMAT(Date, '%b')
ORDER BY STR_TO_DATE(Month, '%b');
    '''
    
    # Execute the query
    return fetch_query_results(db_config, monthly_impact_query)
    

    

#-------------------------------------------------------

def yearly_accident_trends(db_config: Dict[str, str]): #in which accidents has commites more (to done)
    
    yearly_query = f''' 
    SELECT 
    YEAR(`Date`) AS `Year`,  
    COUNT(*) AS `Total_Accidents`, 
    SUM(`Casualties`) AS `Total_Casualties`
FROM `global_traffic_accidents`
WHERE `Date` IS NOT NULL
GROUP BY YEAR(`Date`)
ORDER BY YEAR(`Date`);

    '''
    
    return fetch_query_results(db_config, yearly_query) 

#----------------------------------------------------------------

def derived_accident_severity(db_config: Dict[str, str]): #to change

    severity_query = f''' 
SELECT 
    Accident_Severity,
    COUNT(*) AS Total_Accidents,
    SUM(Casualties) AS Total_Casualties
FROM (
    SELECT 
        CASE 
            WHEN `Casualties` = 0 THEN 'No Injury'
            WHEN `Casualties` BETWEEN 1 AND 2 THEN 'Minor'
            WHEN `Casualties` BETWEEN 3 AND 5 THEN 'Moderate'
            WHEN `Casualties` BETWEEN 6 AND 10 THEN 'Severe'
            ELSE 'Fatal'
        END AS Accident_Severity,
        `Casualties`
    FROM `global_traffic_accidents`
    WHERE `Casualties` IS NOT NULL
) AS Severity_Derived
GROUP BY Accident_Severity
ORDER BY Total_Casualties DESC;

    '''
    
    # Execute the query
    return fetch_query_results(db_config, severity_query)
    


def time_based_analysis(db_config: Dict[str, str]):
    time_query = f''' 
    SELECT 
    HOUR(`Time`) AS `Hour_of_Day`,
    COUNT(*) AS `Total_Accidents`,
    SUM(`Casualties`) AS `Total_Casualties`
FROM `global_traffic_accidents`
WHERE `Time` IS NOT NULL
GROUP BY HOUR(`Time`)
ORDER BY HOUR(`Time`);

    '''
    
    return fetch_query_results(db_config, time_query)
    
    
    
#----------------------------------------------------------- 

def casualties_by_full_time(db_config: Dict[str, str]): # to done create other simmilar

    full_time_query = f''' 
    SELECT 
    CONCAT(`Date`, ' ', `Time`) AS `Full_Timestamp`,
    COUNT(*) AS `Total_Accidents`,
    SUM(`Casualties`) AS `Total_Casualties`
FROM `global_traffic_accidents`
WHERE `Date` IS NOT NULL AND `Time` IS NOT NULL
GROUP BY `Full_Timestamp`
ORDER BY `Full_Timestamp`;

    '''
    

    return fetch_query_results(db_config, full_time_query)


def fetch_all_accident_year(db_config: Dict[str, str]):
    return [ yearly_accident_trends(db_config), derived_accident_severity(db_config), time_based_analysis(db_config), casualties_by_full_time(db_config)]    

    
if __name__ == "__main__":
    # result = casualties_by_full_time(db_config)
    print(accidents_and_casualties_by_month(db_config))
    print("------------")
    print(fetch_all_accident_year(db_config))

