# kaggle_auth.py
import os
import json
from kaggle.api.kaggle_api_extended import KaggleApi

def authenticate_kaggle():
    """Authenticates with the Kaggle API using environment variables."""

    kaggle_username = os.environ.get("KAGGLE_USERNAME")
    kaggle_key = os.environ.get("KAGGLE_KEY")

    if kaggle_username and kaggle_key:
        kaggle_credentials = {
            "username": kaggle_username,
            "key": kaggle_key
        }
        os.makedirs("/root/.config/kaggle", exist_ok=True)
        with open("/root/.config/kaggle/kaggle.json", "w") as f:
            json.dump(kaggle_credentials, f)

        kaggle_api = KaggleApi()
        kaggle_api.authenticate()
        return kaggle_api #return the authenticated api.
    else:
        print("Warning: Kaggle credentials not provided.")
        return KaggleApi() #return the unauthenticated api.