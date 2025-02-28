from ..utils.sql_utils import fetch_query_results , create_new_table
from ..config.db_config import db_config
from typing import Dict

def show_table(db_config:Dict[str,str], table_name: str):
    query: str = f"SELECT * FROM {table_name}"
    return fetch_query_results(db_config, query)


def create_accident_table(db_config:Dict[str,str]):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS accident_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        country VARCHAR(255),
        accident_count INT,
        year INT
    )
    """
    create_new_table(db_config, create_table_query)

def insert_basic_data(db_config:Dict[str,str]):
    insert_data_query = """
    SELECT Location, SUM(Casualties) AS Total_Casualties
    FROM global_traffic_accidents
    GROUP BY Location
    ORDER BY Total_Casualties DESC; 
    """
    # execute_query(db_config, insert_data_query)
    data = fetch_query_results(db_config, insert_data_query)
    print(data)
    

def show_data(db_config:Dict[str,str]):

    data = insert_basic_data(db_config)
    print(data)


if __name__ == "__main__":
    insert_basic_data(db_config)