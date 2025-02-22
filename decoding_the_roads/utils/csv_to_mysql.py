import pandas as pd
from mysql.connector import Error ,MySQLConnection
from mysql.connector.cursor import MySQLCursor
from typing import Dict, List
from ..config.db_connection import create_connection

def insert_data(cursor: MySQLCursor, table_name: str, column_names: list, df: pd.DataFrame) -> None:
    """
    #### Args:
        param cursor: MySQLCursor object 
        param table_name: str 
        param column_names: List[str] 
        param df: pd.DataFrame 

    return: None
    """
    for i, row in df.iterrows():
        sql = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in column_names])}) VALUES ({', '.join(['%s'] * len(row))})"
        cursor.execute(sql, tuple(row)) # Convert the Series to a tuple


def csv_to_mysql(db_config:Dict[str, str], csv_file: str, table_name: str, column_names:List[str])-> None:

    try:
        # Read CSV file into DataFrame
        df = pd.read_csv(csv_file)
        # Create MySQL connection
        connection: MySQLConnection = create_connection(db_config)
        
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor: MySQLCursor = connection.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS `{table_name}` ({', '.join([f'`{col}` TEXT' for col in column_names])})")

            cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
            result = cursor.fetchone()
            if result[0] > 0: # If data is already present in the table
                print(f"Data already present in {table_name} table. Skipping insertion.")
           
            else:
                # * If data is not present in the table
                # * Truncate the table
                cursor.execute(f"TRUNCATE TABLE `{table_name}`")
                print("Table truncated.")
                # Insert data into the table
                insert_data(cursor, table_name, column_names, df)
                print(f"Data from {csv_file} inserted into {table_name} table successfully.")
                connection.commit()
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")