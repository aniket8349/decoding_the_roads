import mysql.connector

from mysql.connector import Error, MySQLConnection, errorcode

from typing import Dict, Optional

def create_connection(db_config: Dict[str, str]) -> Optional[MySQLConnection]:
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
        else:
            print("Failed to connect to MySQL database")
            return None
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print(f"Database '{db_config['database']}' does not exist")
        else:
            print(f"Error: {err}")
        return None