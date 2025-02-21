from ..utils.sql_utils import fetch_query_results , execute_query , create_new_table
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
    INSERT INTO accident_data (country, accident_count, year) VALUES
    ('USA', 1000, 2020),
    ('Canada', 500, 2020),
    ('Mexico', 300, 2020)
    """
    execute_query(db_config, insert_data_query)
    
def show_data(db_config:Dict[str,str]):
      
    create_accident_table(db_config)
    insert_basic_data(db_config)
    data = show_table(db_config, 'accident_data')
    print(data)

