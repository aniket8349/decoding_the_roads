import os
import kaggle

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