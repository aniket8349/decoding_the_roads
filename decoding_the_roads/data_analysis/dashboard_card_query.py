from typing import Dict , List ,Tuple
from ..utils.sql_utils import fetch_query_results , execute_query   



def get_total_accidents_count(db_config: Dict[str, str]) -> int:
    """Fetches the total number of accidents in the database."""
    
    query = """
    SELECT COUNT(*) AS TotalAccidents
    FROM global_traffic_accidents;
    """
    
    # Fetch results
    results = fetch_query_results(db_config, query)
    
    return results[0][0]

def get_highest_accident_locations(db_config: Dict[str, str]) -> List [Tuple[str,int]]:
    """Fetches the highest locations with the highest accident count."""
    
    query = """
    SELECT `Location`, COUNT(*) AS AccidentCount , SUM(`Casualties`) AS TotalCasualties
    FROM global_traffic_accidents 
    GROUP BY `Location`
    ORDER BY AccidentCount DESC 
    LIMIT 1;
    """
    
    # Fetch results
    results = fetch_query_results(db_config, query)
    
    return results

def get_highest_casualties_weather(db_config: Dict[str, str]) -> List [Tuple[str,int]]:
    """Fetches the highest weather conditions with the highest casualties."""
    
    query = """
    SELECT `Weather Condition`, SUM(`Casualties`) AS TotalCasualties
    FROM global_traffic_accidents
    WHERE `Weather Condition` IS NOT NULL
    GROUP BY `Weather Condition`
    ORDER BY TotalCasualties DESC 
    LIMIT 1;
    """
    
    # Fetch results
    results = fetch_query_results(db_config, query)
    
    return results

def get_highest_casualties_cause(db_config: Dict[str, str]) -> List [Tuple[str,int]]:
    """Fetches the highest causes with the highest casualties."""
    
    query = """
    SELECT `Cause`, SUM(`Casualties`) AS TotalCasualties
    FROM global_traffic_accidents
    WHERE `Cause` IS NOT NULL
    GROUP BY `Cause`
    ORDER BY TotalCasualties DESC 
    LIMIT 1;
    """
    
    # Fetch results
    results = fetch_query_results(db_config, query)
    
    return results