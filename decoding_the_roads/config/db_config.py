import os
from dotenv import load_dotenv

load_dotenv()

local = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database':  os.getenv('MYSQL_DATABASE')
}
prod = {
    'host': os.getenv('MYSQL_ADDON_HOST'),
    'user': os.getenv('MYSQL_ADDON_USER'),
    'password': os.getenv('MYSQL_ADDON_PASSWORD'),
    'database':  os.getenv('MYSQL_ADDON_DB')
}


db_config = prod