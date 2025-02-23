from mysql.connector import Error, MySQLConnection
from mysql.connector.cursor import MySQLCursor
from mysql.connector import Error
from typing import Dict

from ..config.db_connection import create_connection

def execute_query(db_config: Dict[str, str], query: str , query_data = None):
    connection: MySQLConnection = create_connection(db_config)
    if connection:
        cursor: MySQLCursor = connection.cursor()
        try:
            if query_data is None:
                cursor.execute(query)
            if query_data:
                cursor.execute(query, query_data)

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
        except Error as err:
            print(f"Error: '{err}'")
            return None
        finally:
            cursor.close()
            connection.close()
    
def fetch_one(db_config: Dict[str, str], query: str ):
    connection = create_connection(db_config)
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            return result
        except Error as err:
            print(f"Error: '{err}'")
            return None
        finally:
            cursor.close()
            connection.close()
def create_new_table(db_config: Dict[str, str], new_table_query: str ):
    execute_query(db_config, new_table_query)


