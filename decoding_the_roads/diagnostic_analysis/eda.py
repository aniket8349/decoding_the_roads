import pandas as pd
from ..config.db_config import db_config
from ..utils.sql_utils import execute_query, fetch_query_results
from typing import Dict 

TABLE_NAME: str = "global_traffic_accidents"

def clean_and_analyze_data(db_config: Dict[str, str]):
    """Performs EDA and data cleaning on the global_traffic_accidents dataset."""
    print(" Running EDA and Data Cleaning Pipeline...")

    queries = {
        "Check Missing Values": """
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


        """,
        
        "check missing value for Accident id":
            '''
            SELECT 
    COUNT(*) AS Missing_Accident_ID
FROM global_traffic_accidents
WHERE `Accident ID` IS NULL; 
''',

        "Remove Missing Values": """
            DELETE FROM global_traffic_accidents 
        WHERE `Weather Condition` IS NULL 
        OR `Road Condition` IS NULL 
        OR `Vehicles Involved` IS NULL 
        OR `Casualties` IS NULL;
""",

        "Remove Duplicates": """
            DELETE t1 
FROM global_traffic_accidents t1
INNER JOIN global_traffic_accidents t2 
ON t1.`Unique_Column` = t2.`Unique_Column` AND t1.rowid > t2.rowid;
""",

        "Top 10 Outliers in Casualties": """
SELECT DISTINCT Casualties 
FROM global_traffic_accidents 
ORDER BY Casualties DESC 
LIMIT 10;

        """,

        "Accident Count by Weather Condition": """
            SELECT `Weather Condition`, COUNT(*) AS Accident_Count
FROM global_traffic_accidents 
WHERE `Weather Condition` IS NOT NULL
GROUP BY `Weather Condition`
ORDER BY Accident_Count DESC;

        """,



        "Accident Severity Distribution": """
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
    }

    results = {}

    for step, query in queries.items():
        print(f" Executing: {step}...")
        try:
            if "SELECT" in query:
                result = fetch_query_results(db_config, query)
                results[step] = result if result else "No Data Found"
            else:
                execute_query(db_config, query)
                results[step] = " Query Executed Successfully"
        except Exception as e:
            print(f" Error in {step}: {e}")
            results[step] = f"Error: {e}"

    print("\n EDA and Cleaning Summary:")
    for step, result in results.items():
        print(f" {step}: {result}\n")

    return results

# Run the function
if __name__ == "__main__":
    eda_results = clean_and_analyze_data(db_config)
