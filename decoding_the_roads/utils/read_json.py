import json
import os
from ..constant.constant import CONTENT_JSON
def read_json_file(file_path):
    """ 
    Function to read a JSON file
    args:
        file_path: str
    returns:
        data 
    """
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            data = json.load(file)
        return data
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)

if __name__ == "__main__":
    file_path = os.path.join(CONTENT_JSON, "content.json")
    data = read_json_file(file_path)
    print(data.get("chart_card1").get("chart_title"))