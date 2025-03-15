import pandas as pd
from ...config.db_config import db_config
from ...utils.sql_utils import execute_query, fetch_query_results
from typing import Dict 


def get_casualties_statistics(db_config: Dict[str, str]):
    """Retrieves mean, median, and mode for casualties in MySQL."""
    
    query = """
    WITH Ranked AS (
        SELECT Casualties, 
            ROW_NUMBER() OVER (ORDER BY Casualties) AS RowAsc,
            ROW_NUMBER() OVER (ORDER BY Casualties DESC) AS RowDesc,
            COUNT(*) OVER () AS TotalRows
        FROM global_traffic_accidents
    )
    SELECT 
        AVG(Casualties) AS MeanCasualties,
        (SELECT Casualties FROM Ranked WHERE RowAsc = CEIL(TotalRows / 2) LIMIT 1) AS MedianCasualties
    FROM global_traffic_accidents;
    """
    
    mode_query = """
    SELECT Casualties 
    FROM global_traffic_accidents 
    GROUP BY Casualties 
    ORDER BY COUNT(*) DESC 
    LIMIT 1;
    """
    
    results = fetch_query_results(db_config, query)
    mode_result = fetch_query_results(db_config, mode_query)

    if results and mode_result:
        return pd.DataFrame(
            [{"Mean Casualties": results[0][0], "Median Casualties": results[0][1], "Mode Casualties": mode_result[0][0]}]
        )
    else:
        return pd.DataFrame(columns=["Mean Casualties", "Median Casualties", "Mode Casualties"])
#---------------------------------------------------------------------------------------------------------------

def get_vehicles_statistics(db_config: Dict[str, str]):
    """Retrieves mean, median, and mode for vehicles involved in accidents."""
    
    query = """
    WITH Ranked AS (
        SELECT `Vehicles Involved`, 
            ROW_NUMBER() OVER (ORDER BY `Vehicles Involved`) AS RowAsc,
            ROW_NUMBER() OVER (ORDER BY `Vehicles Involved` DESC) AS RowDesc,
            COUNT(*) OVER () AS TotalRows
        FROM global_traffic_accidents
    )
    SELECT 
        AVG(`Vehicles Involved`) AS MeanVehicles,
        (SELECT `Vehicles Involved` FROM Ranked WHERE RowAsc = CEIL(TotalRows / 2) LIMIT 1) AS MedianVehicles
    FROM global_traffic_accidents;
    """
    
    mode_query = """
    SELECT `Vehicles Involved`
    FROM global_traffic_accidents 
    GROUP BY `Vehicles Involved` 
    ORDER BY COUNT(*) DESC 
    LIMIT 1;
    """
    
    results = fetch_query_results(db_config, query)
    mode_result = fetch_query_results(db_config, mode_query)
    
    if results and mode_result:
        return pd.DataFrame(
            [{"Mean Vehicles": results[0][0], "Median Vehicles": results[0][1], "Mode Vehicles": mode_result[0][0]}]
        )
    else:
        return pd.DataFrame(columns=["Mean Vehicles", "Median Vehicles", "Mode Vehicles"])

#--------------------------------------------------------------------------------------------------


def get_accidents_per_location(db_config: Dict[str, str]):
    """Finds total accidents per location."""
    
    query = """
    SELECT Location, COUNT(*) AS TotalAccidents
    FROM global_traffic_accidents
    GROUP BY Location
    ORDER BY TotalAccidents DESC
    LIMIT 10;
    """
    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Location", "Total Accidents"])

#------------------------------------------------------------------------------------

def get_accidents_per_weather(db_config: Dict[str, str]):
    """Finds total accidents per weather condition."""
    
    query = """
    SELECT `Weather Condition`, COUNT(*) AS TotalAccidents
    FROM global_traffic_accidents
    GROUP BY `Weather Condition`
    ORDER BY TotalAccidents DESC;
    """
    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Weather Condition", "Total Accidents"])
#----------------------------------------------------------------------------------


def get_frequency_distributions_weather(db_config: Dict[str, str]):
    """Retrieves accident frequency based on weather conditions and time of day."""
    
    weather_query = """
    SELECT `Weather Condition`, COUNT(*) AS AccidentCount
    FROM global_traffic_accidents
    GROUP BY `Weather Condition`
    ORDER BY AccidentCount DESC;
    """
    
    results = fetch_query_results(db_config, weather_query)
    return pd.DataFrame(results, columns=["Weather Condition", "Accident Count"])
    
#----------------------------------------------------------------------------------------
def get_frequency_distributions_time(db_config: Dict[str, str]):

    time_query = """
    SELECT 
        CASE 
            WHEN HOUR(`Time`) BETWEEN 0 AND 5 THEN 'Midnight - Early Morning'
            WHEN HOUR(`Time`) BETWEEN 6 AND 11 THEN 'Morning'
            WHEN HOUR(`Time`) BETWEEN 12 AND 17 THEN 'Afternoon'
            WHEN HOUR(`Time`) BETWEEN 18 AND 23 THEN 'Evening - Night'
        END AS TimeOfDay,
        COUNT(*) AS AccidentCount
    FROM global_traffic_accidents
    GROUP BY TimeOfDay
    ORDER BY AccidentCount DESC;
    """    
    result = fetch_query_results(db_config, time_query)  
    return pd.DataFrame(result, columns=["Time of Day", "Accident Count"])
    
if __name__ == "__main__":
    df =get_frequency_distributions_time(db_config)
    print(df)

