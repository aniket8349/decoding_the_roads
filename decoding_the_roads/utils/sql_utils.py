from mysql.connector import Error
from typing import Dict
from ..config.db_connection import create_connection

def execute_query(db_config: Dict[str, str], query: str ):
    connection = create_connection(db_config)
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
        except Error as err:
            print(f"Error: '{err}'")
        finally:
            cursor.close()
            connection.close()

def fetch_query_results(db_config: Dict[str, str], query: str ):
    connection = create_connection(db_config)
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as err:
            print(f"Error: '{err}'")
            return None
        finally:
            cursor.close()
            connection.close()

def create_new_table(db_config: Dict[str, str], new_table_query: str ):
    execute_query(db_config, new_table_query)


