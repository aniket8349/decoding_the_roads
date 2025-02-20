import os
import kaggle
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

from .config.db_config import db_config
from .utils.csv_to_mysql import csv_to_mysql
from .utils.get_column_names import get_column_names
from .data_analysis.accident_trends import show_data


load_dotenv() # loading env

api = KaggleApi()
api.authenticate()

DATA_DIR = "./data/raw" 
PROCESSED_DATA_DIR = "./data/processed"
MODELS_DIR = "./models"
REPORTS_DIR = "./reports"

def download_data(dataset_slug, data_dir):
    
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

        
def main():

    print("Hi starting...!")
    
    table_name = 'global_traffic_accidents'
    csv_file = os.path.join(DATA_DIR, "global_traffic_accidents.csv")
    
    dataset_slug = os.getenv("KAGGLE_DATASET_SLUG")
    download_data(dataset_slug, DATA_DIR)
    
    # print(db_config)
    # check_mysql_connection(db_config)
    column_list = get_column_names(csv_file)
    print(column_list)
    if column_list:
        csv_to_mysql(db_config, csv_file, table_name, column_list)
    else:
        print("Failed to get column names from CSV file.")
        
    show_data(db_config)



if __name__ == "__main__":
    main()