import pandas as pd
from ..config.db_config import db_config
from ..utils.sql_utils import execute_query, fetch_query_results
from typing import Dict 

TABLE_NAME: str = "global_traffic_accidents"

def check_missing_values(db_config: Dict[str, str]) :
    """Check missing values in the global_traffic_accidents dataset."""
    query = """
        SELECT 
            SUM(CASE WHEN `Cause` IS NULL THEN 1 ELSE 0 END) AS Missing_Cause, 
            SUM(CASE WHEN `Weather Condition` IS NULL THEN 1 ELSE 0 END) AS Missing_Weather,
            SUM(CASE WHEN `Road Condition` IS NULL THEN 1 ELSE 0 END) AS Missing_Road,
            SUM(CASE WHEN `Vehicles Involved` IS NULL THEN 1 ELSE 0 END) AS Missing_Vehicles,
            SUM(CASE WHEN `Casualties` IS NULL THEN 1 ELSE 0 END) AS Missing_Casualties,
            SUM(CASE WHEN `Location` IS NULL THEN 1 ELSE 0 END) AS Missing_Location,
            SUM(CASE WHEN `Date` IS NULL THEN 1 ELSE 0 END) AS Missing_Date,
            SUM(CASE WHEN `Time` IS NULL THEN 1 ELSE 0 END) AS Missing_Time
        FROM global_traffic_accidents;
    """
    try:
        result = fetch_query_results(db_config, query)
        if not result or not result[0]:  # Check if result is empty
            return {}

        # Extract first row (tuple of Decimals) and convert to an int dictionary
        missing_values: Dict[str,int] = {
            "Missing_Cause": int(result[0][0]),
            "Missing_Weather": int(result[0][1]),
            "Missing_Road": int(result[0][2]),
            "Missing_Vehicles": int(result[0][3]),
            "Missing_Casualties": int(result[0][4]),
            "Missing_Location": int(result[0][5]),
            "Missing_Date": int(result[0][6]),
            "Missing_Time": int(result[0][7]),
        }
        return missing_values if missing_values else "No Data Found"
    except Exception as e:
        return f"Error: {e}"

def check_missing_value_for_accident_id(db_config: Dict[str, str]):
    """Check missing value for Accident ID in the global_traffic_accidents dataset."""
    query = """
        SELECT 
            COUNT(*) AS Missing_Accident_ID
        FROM global_traffic_accidents
        WHERE `Accident ID` IS NULL; 
    """
    try:
        result = fetch_query_results(db_config, query)
        return result if result else "No Data Found"
    except Exception as e:
        return f"Error: {e}"

def remove_missing_values(db_config: Dict[str, str]):
    """Remove rows with missing values in the global_traffic_accidents dataset."""
    query = """
        DELETE FROM global_traffic_accidents 
        WHERE `Weather Condition` IS NULL 
        OR `Road Condition` IS NULL 
        OR `Vehicles Involved` IS NULL 
        OR `Casualties` IS NULL;
    """
    try:
        execute_query(db_config, query)
        return "Query Executed Successfully"
    except Exception as e:
        return f"Error: {e}"

def remove_duplicates(db_config: Dict[str, str]) :
    """Remove duplicate rows in the global_traffic_accidents dataset."""
    query = """
        DELETE t1 
        FROM global_traffic_accidents t1
        INNER JOIN global_traffic_accidents t2 
        ON t1.`Unique_Column` = t2.`Unique_Column` AND t1.rowid > t2.rowid;
    """
    try:
        execute_query(db_config, query)
        return "Query Executed Successfully"
    except Exception as e:
        return f"Error: {e}"

def get_top_10_outliers_in_casualties(db_config: Dict[str, str]) :
    """Get the top 10 outliers in Casualties in the global_traffic_accidents dataset."""
    query = """
        SELECT DISTINCT Casualties 
        FROM global_traffic_accidents 
        ORDER BY Casualties DESC 
        LIMIT 10;
    """
    try:
        result = fetch_query_results(db_config, query)
        return result if result else "No Data Found"
    except Exception as e:
        return f"Error: {e}"

def get_accident_count_by_weather_condition(db_config: Dict[str, str]) :
    """Get the accident count by Weather Condition in the global_traffic_accidents dataset."""
    query = """
        SELECT `Weather Condition`, COUNT(*) AS Accident_Count
        FROM global_traffic_accidents 
        WHERE `Weather Condition` IS NOT NULL
        GROUP BY `Weather Condition`
        ORDER BY Accident_Count DESC;
    """
    try:
        result = fetch_query_results(db_config, query)
        return result if result else "No Data Found"
    except Exception as e:
        return f"Error: {e}"

def get_accident_severity_distribution(db_config: Dict[str, str]) :
    """Get the accident severity distribution in the global_traffic_accidents dataset."""
    query = """
        SELECT 
            CASE 
                WHEN Casualties = 0 THEN 'No Injury'
                WHEN Casualties BETWEEN 1 AND 3 THEN 'Minor'
                WHEN Casualties BETWEEN 4 AND 10 THEN 'Severe'
                ELSE 'Fatal'
            END AS Severity,
            COUNT(*) AS Accident_Count
        FROM global_traffic_accidents
        GROUP BY Severity;
    """
    try:
        result = fetch_query_results(db_config, query)
        return result if result else "No Data Found"
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print("Running EDA and Data Cleaning Pipeline...")
    results = check_missing_value_for_accident_id(db_config)
    print(results)
