
import pandas as pd
from ..config.db_config import db_config
from ..utils.sql_utils import execute_query, fetch_query_results
from typing import Dict 

def get_accident_hotspots(db_config: Dict[str, str]):
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




# if __name__ == "__main__":
#     df =get_high_risk_times(db_config)
#     print(df)
