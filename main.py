import kaggle
import os
from dotenv import load_dotenv
from kaggle.api.kaggle_api_extended import KaggleApi

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
    dataset_slug = os.getenv("KAGGLE_DATASET_SLUG")
    download_data(dataset_slug, DATA_DIR)

if __name__ == "__main__":
    main()