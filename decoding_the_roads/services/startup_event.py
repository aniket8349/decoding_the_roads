import os

from ..config.db_config import db_config
from ..utils.csv_to_mysql import csv_to_mysql
from ..utils.get_column_names import get_column_names
from ..config.download_data import download_data
from ..constant.constant import TABLE_NAME, DATA_DIR
from ..utils.sql_utils import fetch_one
from ..utils.logger import setup_logger

logger = setup_logger(__name__)  

async def startup_event():

    logger.info("Starting up...")

    try:

        csv_file: str = os.path.join(DATA_DIR, "global_traffic_accidents.csv")
        dataset_slug: str = os.getenv("KAGGLE_DATASET_SLUG")

        # check if database does not exist
        check_databases = fetch_one(db_config, f"SHOW DATABASES LIKE '{db_config['database']}'")
        if not check_databases:
            
            download_data(dataset_slug, DATA_DIR)  # Pass kaggle_api to download function

            column_list = get_column_names(csv_file)
            if column_list:
                csv_to_mysql(db_config, csv_file, TABLE_NAME, column_list)
            else:
                raise RuntimeError("Failed to get column names from CSV file.")

        logger.info("Startup complete.")

    except Exception as e:  # Catch potential startup errors
        logger.error(f"Startup error: {e}")
        raise RuntimeError("Startup error")  # Raise an exception to stop the app

