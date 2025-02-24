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
    
    # Print the results
    



def yearly_accident_trends(db_config: Dict[str, str]): #in which accidents has commites more
    
    yearly_query = f''' 
    SELECT 
        "Year", 
        COUNT(*) AS accident_count, 
        SUM("Casualties") AS total_casualties
    FROM `{TABLE_NAME}`
    GROUP BY "Year"
    ORDER BY "Year";
    '''
    
    return fetch_query_results(db_config, yearly_query)
    
    
    
    

def derived_accident_severity(db_config: Dict[str, str]):

    severity_query = f''' 
    SELECT 
        CASE 
            WHEN "Casualties" = 0 THEN 'No Injury'
            WHEN "Casualties" BETWEEN 1 AND 2 THEN 'Minor'
            WHEN "Casualties" BETWEEN 3 AND 5 THEN 'Moderate'
            WHEN "Casualties" BETWEEN 6 AND 10 THEN 'Severe'
            ELSE 'Fatal'
        END AS "Accident Severity",
        COUNT(*) AS accident_count,
        SUM("Casualties") AS total_casualties
    FROM `{TABLE_NAME}`
    GROUP BY "Accident Severity"
    ORDER BY total_casualties DESC;
    '''
    
    # Execute the query
    return fetch_query_results(db_config, severity_query)
    
    
    
    
    

def time_based_analysis(db_config: Dict[str, str]):

    time_query = f''' 
    SELECT 
        "Hour" AS "Time Period",
        'Hour' AS "Category",
        COUNT(*) AS accident_count, 
        SUM("Casualties") AS total_casualties
    FROM `{TABLE_NAME}`
    GROUP BY "Hour"

    UNION ALL

    SELECT 
        "Day of Week" AS "Time Period",
        'Day of Week' AS "Category",
        COUNT(*) AS accident_count, 
        SUM("Casualties") AS total_casualties
    FROM `{TABLE_NAME}`
    GROUP BY "Day of Week"

    ORDER BY accident_count DESC;
    '''
    
    return fetch_query_results(db_config, time_query)
    
    
    
    

def casualties_by_full_time(db_config: Dict[str, str]):

    full_time_query = f''' 
    SELECT 
        TIME_FORMAT("Timestamp", '%H:%i:%s') AS full_time, 
        SUM("Casualties") AS total_casualties
    FROM `{TABLE_NAME}`
    GROUP BY full_time
    ORDER BY total_casualties DESC;
    '''
    

    return fetch_query_results(db_config, full_time_query)

    

    
if __name__ == "__main__":
    result = accidents_and_casualties_by_month(db_config)
    
    
    
    
