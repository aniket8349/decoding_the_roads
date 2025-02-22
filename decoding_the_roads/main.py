import os
import kaggle
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi
from .config.db_config import db_config
from .utils.csv_to_mysql import csv_to_mysql
from .utils.get_column_names import get_column_names
from .data_analysis.accident_trends import show_data

from typing import List, Optional

load_dotenv() # loading env

api = KaggleApi()
api.authenticate()

DATA_DIR: str = "./data/raw" 
PROCESSED_DATA_DIR: str = "./data/processed"
MODELS_DIR: str = "./models"
REPORTS_DIR: str = "./reports"

def download_data(dataset_slug: str, data_dir: str):
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Check if dataset is already downloaded
    if len(os.listdir(data_dir)) > 0:
        print("Dataset already downloaded.")
        return

    print(f"Downloading dataset {dataset_slug}...")
    try:
        kaggle.api.dataset_download_files(dataset_slug, path=data_dir, unzip=True)
        print("Dataset downloaded successfully.")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        exit(1)

        
def main() -> None:

    print("Hi starting...!")
    
    table_name: str = 'global_traffic_accidents'
    csv_file: str = os.path.join(DATA_DIR, "global_traffic_accidents.csv")
    
    dataset_slug: str = os.getenv("KAGGLE_DATASET_SLUG")
    
    download_data(dataset_slug, DATA_DIR)
    
    # print(db_config)
    # check_mysql_connection(db_config)
    column_list: List[str] = get_column_names(csv_file)
    print(column_list)
    if column_list:
        csv_to_mysql(db_config, csv_file, table_name, column_list)
    else:
        print("Failed to get column names from CSV file.")
        
    # show_data(db_config)



if __name__ == "__main__":
    main()