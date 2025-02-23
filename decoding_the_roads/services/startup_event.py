import os

from ..config.db_config import db_config
from ..utils.csv_to_mysql import csv_to_mysql
from ..utils.get_column_names import get_column_names
from ..config.download_data import download_data
from ..constant.constant import TABLE_NAME, DATA_DIR



async def startup_event():

    print("Starting up...")

    try:

        csv_file: str = os.path.join(DATA_DIR, "global_traffic_accidents.csv")
        dataset_slug: str = os.getenv("KAGGLE_DATASET_SLUG")

        download_data(dataset_slug, DATA_DIR)  # Pass kaggle_api to download function

        column_list = get_column_names(csv_file)
        if column_list:
            csv_to_mysql(db_config, csv_file, TABLE_NAME, column_list)
        else:
            raise RuntimeError("Failed to get column names from CSV file.")

        print("Startup complete.")

    except Exception as e:  # Catch potential startup errors
        print(f"Startup error: {e}")
        raise  # Re-raise the exception to prevent the app from starting

