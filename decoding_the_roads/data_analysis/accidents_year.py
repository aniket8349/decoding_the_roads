from ..utils.sql_utils import create_new_table , execute_query , fetch_query_results
from typing import Dict 



#Identifying the year and month of most accidents count and causalties 
TABLE_NAME: str = "global_traffic_accidents"

def accidents_and_casualties_by_month(db_config: Dict[str, str]):#accidents_and_casualties_by_month
    monthly_impact_query = f''' 
    SELECT 
    "Month", 
    COUNT(*) AS accident_count, 
    SUM("Casualties") AS total_casualties
    FROM `{TABLE_NAME}`
    GROUP BY "Month"
    ORDER BY total_casualties DESC;
    '''
    
    # Execute the query
    result = fetch_query_results(db_config, monthly_impact_query)
    
    # Print the results
    print(result)
    

from typing import Dict

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
    
    result = fetch_query_results(db_config, yearly_query)
    print(result)
    
    
    from typing import Dict

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
    result = fetch_query_results(db_config, severity_query)
    
    # Print the results
    print(result)
    
    from typing import Dict

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
    
    result = fetch_query_results(db_config, time_query)
    print(result)
