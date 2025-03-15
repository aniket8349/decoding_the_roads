
import pandas as pd
from typing import Dict

from ...config.db_config import db_config
from ...utils.sql_utils import fetch_query_results


#Correlation Analysis
def get_avg_casualties_by_weather(db_config: Dict[str, str]):
    """Fetches the average number of casualties for each weather condition."""
    
    query = """
    SELECT `Weather Condition`, AVG(`Casualties`) AS Avg_Casualties
    FROM global_traffic_accidents 
    GROUP BY `Weather Condition`
    ORDER BY Avg_Casualties DESC;
    """
    
    results = fetch_query_results(db_config, query)
    return results
    # return pd.DataFrame(results, columns=["Weather Condition", "Avg Casualties"])


def get_accident_counts_by_time_period(db_config: Dict[str, str]):
    """
    Categorizes accidents into different time periods based on the hour of the accident and counts the number of accidents in each period.
    """
    query = """
    SELECT 
        CASE 
            WHEN CAST(SUBSTR(Time, 1, 2) AS SIGNED) BETWEEN 0 AND 6 THEN 'Midnight-6AM'
            WHEN CAST(SUBSTR(Time, 1, 2) AS SIGNED) BETWEEN 7 AND 12 THEN 'Morning'
            WHEN CAST(SUBSTR(Time, 1, 2) AS SIGNED) BETWEEN 13 AND 18 THEN 'Afternoon'
            ELSE 'Evening'
        END AS TimePeriod,
        COUNT(*) AS AccidentCount
    FROM global_traffic_accidents
    GROUP BY TimePeriod
    ORDER BY AccidentCount DESC;
    """
    
    result = fetch_query_results(db_config, query)
    return result
    # return pd.DataFrame(result, columns=["TimePeriod", "AccidentCount"])


#Root Cause & Comparative Analysis
def get_top_accident_prone_locations(db_config: Dict[str, str]):
    """Fetches the top 10 accident-prone locations based on the number of accidents and casualties."""
    
    query = """
    SELECT `Location`, COUNT(*) AS AccidentCount, SUM(`Casualties`) AS TotalCasualties
    FROM global_traffic_accidents 
    GROUP BY `Location`
    ORDER BY AccidentCount DESC 

    """
    
    # Fetch results
    results = fetch_query_results(db_config, query)
    
    # # Convert to DataFrame
    # return pd.DataFrame(results, columns=["Location", "Accident Count", "Total Casualties"])
    return results

def get_most_dangerous_times(db_config: Dict[str, str]):
    """Fetches the top 5 most dangerous hours of the day based on accident count."""
    
    query = """
    SELECT SUBSTR(`Time`, 1, 2) AS Hour, COUNT(*) AS AccidentCount 
    FROM global_traffic_accidents
    GROUP BY Hour 
    ORDER BY AccidentCount DESC 
    LIMIT 5;
    """
    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Hour", "Accident Count"])

def get_most_dangerous_weather_conditions(db_config: Dict[str, str]):
    """Fetches the top 5 most dangerous weather conditions based on casualties."""
    
    query = """
    SELECT `Weather Condition`, SUM(`Casualties`) AS TotalCasualties, COUNT(*) AS TotalAccidents 
    FROM global_traffic_accidents
    GROUP BY `Weather Condition` 
    ORDER BY TotalCasualties DESC 
    LIMIT 5;
    """
    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Weather Condition", "Total Casualties", "Total Accidents"])
    
#Hypothesis Testing
#Does Rainy Weather Increase Accidents?
def get_accidents_clear_vs_rainy(db_config: Dict[str, str]):
    """Fetches the count of accidents in clear vs. rainy weather."""
    
    query = """
    SELECT `Weather Condition`, COUNT(*) AS AccidentCount 
    FROM global_traffic_accidents 
    WHERE `Weather Condition` IN ('Clear', 'Rain') 
    GROUP BY `Weather Condition`;
    """
    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Weather Condition", "Accident Count"])


#Are More Vehicles Involved in Accidents on Wet Roads?
def get_avg_vehicles_by_road_condition(db_config: Dict[str, str]):
    """Fetches the average number of vehicles involved in accidents for each road condition."""
    
    query = """
    SELECT `Road Condition`, AVG(`Vehicles Involved`) AS AvgVehicles 
    FROM global_traffic_accidents 
    GROUP BY `Road Condition`
    ORDER BY AvgVehicles DESC;
    """
    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Road Condition", "Avg Vehicles Involved"])


#Insights & Recommendations

# Find the most common causes of accidents
def get_common_accident_causes(db_config: Dict[str, str]):
    """Fetches the top 5 most common causes of accidents based on occurrence count."""
    
    query = """
    SELECT `Cause`, COUNT(*) AS AccidentCount 
    FROM global_traffic_accidents 
    GROUP BY `Cause`
    ORDER BY AccidentCount DESC 
    LIMIT 5;
    """
    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Cause", "Accident Count"])


#Which locations need road safety improvements?
def get_locations_needing_safety_improvements(db_config: Dict[str, str]):
    """Fetches the top 10 locations with the most accidents in hazardous road conditions."""
    
    query = """
    SELECT `Location`, `Road Condition`, COUNT(*) AS AccidentCount 
    FROM global_traffic_accidents 
    WHERE `Road Condition` IN ('Wet', 'Icy', 'Snowy') 
    GROUP BY `Location`, `Road Condition` 
    ORDER BY AccidentCount DESC 
    LIMIT 10;
    """
    
    results = fetch_query_results(db_config, query)
    return pd.DataFrame(results, columns=["Location", "Road Condition", "Accident Count"])

# Example usage
if __name__ == "__main__":
    df =get_locations_needing_safety_improvements(db_config)
    print(df)
