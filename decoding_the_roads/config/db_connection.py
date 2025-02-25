import mysql.connector

from mysql.connector import Error, MySQLConnection, errorcode
from typing import Dict, Optional

from ..utils.logger import setup_logger

logger = setup_logger(__name__)  # No log_file argument, so it logs to terminal

def create_connection(db_config: Dict[str, str]) -> Optional[MySQLConnection]:
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        if connection.is_connected():
            logger.info("Successfully connected to MySQL database")
            return connection
        else:
            logger.info("Failed to connect to MySQL database")
            return None
    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.error("Error: Access denied")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.error(f"Database '{db_config['database']}' does not exist")
        else:
            logger.error(f"Error: {err}")
        return None