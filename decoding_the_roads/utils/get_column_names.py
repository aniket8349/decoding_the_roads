import pandas as pd
from typing import List, Optional

def get_column_names(csv_file_path: str) -> Optional[List[str]]:
    """
    Extracts column names from a CSV file using pandas.

    Args:
        csv_file_path: The path to the CSV file.

    Returns:
        A list of column names, or None if there's an error.
    """
    try:
        df = pd.read_csv(csv_file_path)  # Read the CSV into a pandas DataFrame
        column_names = df.columns.tolist()  # Get the column names as a list
        return column_names
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_file_path}")
        return None
    except pd.errors.EmptyDataError:  
        print(f"Error: CSV file is empty: {csv_file_path}")
        return None
    except Exception as e:  
        print(f"An error occurred: {e}")
        return None

