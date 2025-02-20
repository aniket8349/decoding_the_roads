import pandas as pd
import mysql.connector
from mysql.connector import Error
from ..config.db_connection import create_connection


def csv_to_mysql(db_config, csv_file, table_name, column_names):
    try:
        # Read CSV file into DataFrame
        df = pd.read_csv(csv_file)
        
 
        connection = create_connection(db_config)
        
        if connection.is_connected():
            print("Connected to MySQL database")
            cursor = connection.cursor()
            cursor.execute(f"CREATE TABLE IF NOT EXISTS `{table_name}` ({', '.join([f'`{col}` TEXT' for col in column_names])})")

            for i, row in df.iterrows():
                sql = f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in column_names])}) VALUES ({', '.join(['%s'] * len(row))})"
                cursor.execute(sql, tuple(row))

            connection.commit()
            print(f"Data from {csv_file} inserted into {table_name} table successfully.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")