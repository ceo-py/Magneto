import requests
from dotenv import dotenv_values, find_dotenv

CONFIG = dotenv_values(find_dotenv())
EZTVX_URL = CONFIG["EZTVX_URL"]


def get_serials_eztvx(imdb_id:str ) -> list:
    
    with requests.get(f"{EZTVX_URL}{imdb_id}") as response:
        if response.status_code == 200:
            data = response.json()
            return data.get("torrents", [])
        else:
            return []
