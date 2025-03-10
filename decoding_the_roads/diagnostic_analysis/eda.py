from ..utils.sql_utils import create_new_table , execute_query , fetch_query_results
from ..config.db_config import db_config
from typing import Dict 


#Exploratory Data Analysis (EDA)
def exploratory_data_analysis(db_config: Dict[str, str]):
    query = """
    SELECT 
        COUNT(*) AS Total_Accidents, 
        SUM(Casualties) AS Total_Casualties, 
        AVG(`Vehicles Involved`) AS Avg_Vehicles_Per_Accident
    FROM global_traffic_accidents;
    """
    return fetch_query_results(db_config, query)


def accidents_by_weather(db_config: Dict[str, str]):
    query = """
    SELECT 
        `Weather Condition`, 
        COUNT(*) AS Total_Accidents, 
        SUM(Casualties) AS Total_Casualties
    FROM global_traffic_accidents
    GROUP BY `Weather Condition`
    ORDER BY Total_Accidents DESC;
    """
    return fetch_query_results(db_config, query)


#Root Cause & Comparative Analysis
def high_risk_locations(db_config: Dict[str, str]):
    query = """
    SELECT 
        Location, 
        COUNT(*) AS Total_Accidents, 
        SUM(Casualties) AS Total_Casualties
    FROM global_traffic_accidents
    WHERE Location IS NOT NULL
    GROUP BY Location
    ORDER BY Total_Accidents DESC
    LIMIT 10;
    """
    return fetch_query_results(db_config, query)

def time_based_analysis(db_config: Dict[str, str]):
    query = """
    SELECT 
        CASE 
            WHEN HOUR(Time) BETWEEN 0 AND 6 THEN 'Midnight (12 AM - 6 AM)'
            WHEN HOUR(Time) BETWEEN 7 AND 12 THEN 'Morning (7 AM - 12 PM)'
            WHEN HOUR(Time) BETWEEN 13 AND 18 THEN 'Afternoon (1 PM - 6 PM)'
            ELSE 'Evening/Night (7 PM - 11 PM)'
        END AS Time_Period, 
        COUNT(*) AS Total_Accidents, 
        SUM(Casualties) AS Total_Casualties
    FROM global_traffic_accidents
    GROUP BY Time_Period
    ORDER BY Total_Accidents DESC;
    """
    return fetch_query_results(db_config, query)


#Hypothesis Testing (Data Preparation for Python T-Test or ANOVA)
def accident_weather_analysis(db_config: Dict[str, str]):
    query = """
    SELECT 
        `Weather Condition`, 
        COUNT(*) AS Total_Accidents, 
        AVG(`Vehicles Involved`) AS Avg_Vehicles,
        AVG(Casualties) AS Avg_Casualties
    FROM global_traffic_accidents
    WHERE `Weather Condition` IN ('Rain', 'Clear')
    GROUP BY `Weather Condition`;
    """
    return fetch_query_results(db_config, query)

# Insights & Recommendations
def common_accident_causes(db_config: Dict[str, str]):
    query = """
    SELECT 
        Cause, 
        COUNT(*) AS Total_Accidents, 
        SUM(Casualties) AS Total_Casualties
    FROM global_traffic_accidents
    GROUP BY Cause
    ORDER BY Total_Accidents DESC
    LIMIT 10;
    """
    return fetch_query_results(db_config, query)

def accident_hotspots(db_config: Dict[str, str]):
    query = """
    SELECT 
        Location, 
        SUM(Casualties) AS Total_Casualties, 
        COUNT(*) AS Total_Accidents
    FROM global_traffic_accidents
    GROUP BY Location
    ORDER BY Total_Casualties DESC
    LIMIT 10;
    """
    return fetch_query_results(db_config, query)


if __name__ == "__main__":
    result = common_accident_causes(db_config)
    print(result)
