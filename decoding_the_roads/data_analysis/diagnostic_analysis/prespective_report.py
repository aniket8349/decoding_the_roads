
import pandas as pd
from ...config.db_config import db_config
from ...utils.sql_utils import execute_query, fetch_query_results
from typing import Dict 

# accident-prone areas based on geographical distribution

def get_accident_prone_longitudinal(db_config: Dict[str, str]):
    query = f"""SELECT 
    Latitude, 
    Longitude, 
    COUNT(Accident_ID) AS Accident_Count
FROM accidents
GROUP BY Latitude, Longitude
ORDER BY Accident_Count DESC;
"""
    results = fetch_query_results(db_config, query)
# TODO only two coloumn for density map need three coloumn
def get_accident_hotspots(db_config: Dict[str, str]):            #get_accident_prone_location
    """Finds locations with the highest accident occurrences."""
    
    query = """
    SELECT Location, COUNT(*) AS AccidentCount
    FROM global_traffic_accidents 
    GROUP BY Location
    ORDER BY AccidentCount DESC
    LIMIT 10;
"""
    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Location", "Accident Count"])

def get_high_risk_times(db_config: Dict[str, str]):
    """Finds peak hours for accidents."""
    
    query = """
    SELECT SUBSTR(Time, 1, 2) AS Hour, COUNT(*) AS AccidentCount
    FROM global_traffic_accidents
    GROUP BY Hour
    ORDER BY AccidentCount DESC
    LIMIT 5;
    """
    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Hour", "Accident Count"])

def get_weather_related_accidents(db_config: Dict[str, str]):
    """Finds weather conditions contributing to high accident rates."""
    
    query = """
    SELECT `Weather Condition`, COUNT(*) AS AccidentCount, AVG(`Casualties`) AS AvgCasualties
FROM `global_traffic_accidents`
GROUP BY `Weather Condition`
ORDER BY AccidentCount DESC
LIMIT 5;

    """
    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Weather Condition", "Accident Count", "Avg Casualties"])

def get_high_severity_accidents(db_config: Dict[str, str]):
    """Finds conditions leading to severe accidents."""
    
    query = """
    SELECT `Road Condition`, AVG(Casualties) AS AvgCasualties, COUNT(*) AS TotalAccidents
    FROM global_traffic_accidents
    GROUP BY `Road Condition`
    ORDER BY AvgCasualties DESC
    LIMIT 5;
    """
    

    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Road Condition", "Avg Casualties", "Total Accidents"])


def  accidets_by_time_weather_condition(db_config: Dict[str, str]):
    """Finds weather conditions contributing to high accident rates."""
    
    query = """
    SELECT 
    CASE 
        WHEN HOUR(Time) BETWEEN 0 AND 5 THEN 'Midnight-6AM'
        WHEN HOUR(Time) BETWEEN 6 AND 11 THEN 'Morning'
        WHEN HOUR(Time) BETWEEN 12 AND 17 THEN 'Afternoon'
        WHEN HOUR(Time) BETWEEN 18 AND 23 THEN 'Evening'
    END AS TimePeriod,
    `Weather Condition`,
    COUNT(`Accident ID`) AS Accident_Count
FROM global_traffic_accidents
GROUP BY 
    CASE 
        WHEN HOUR(Time) BETWEEN 0 AND 5 THEN 'Midnight-6AM'
        WHEN HOUR(Time) BETWEEN 6 AND 11 THEN 'Morning'
        WHEN HOUR(Time) BETWEEN 12 AND 17 THEN 'Afternoon'
        WHEN HOUR(Time) BETWEEN 18 AND 23 THEN 'Evening'
    END,
    `Weather Condition`
ORDER BY Accident_Count DESC;



    """
    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["TimePeriod", "Weather Condition", "Accident Count"])



def road_caondition_vs_vehicles_involved(db_config: Dict[str, str]):
    """Finds conditions leading to severe accidents."""
    
    query = """
    SELECT 
    `Road Condition`,
    `Vehicles Involved`,
    COUNT(`Accident ID`) AS Accident_Count
FROM global_traffic_accidents
GROUP BY `Road Condition`, `Vehicles Involved`
ORDER BY Accident_Count DESC;

    """
    

    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Road Condition", "Vehicles Involved", "Accident_Count"])


if __name__ == "__main__":
    df =road_caondition_vs_vehicles_involved(db_config)
    print(df)
