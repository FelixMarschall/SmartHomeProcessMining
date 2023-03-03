import requests
import pandas as pd
import logging
import os

host = "homeassistant.local"
port = 8123
internal_host = "http://supervisor/core/api/"
url = f"http://{host}:{port}/api/"

timestamp = "2022-02-15T00:00:00+02:00"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIzMzc5NDBmZmZlNWU0MWJiYmY4MDZmYzYzZmM0MjNhNSIsImlhdCI6MTY3NzcwNjg4MSwiZXhwIjoxOTkzMDY2ODgxfQ.IrgtgxwY1dKjTcNV59ZhX-URvptsQ_MmE6XsPN-23WA"

super_token = False
if 'SUPERVISOR_TOKEN' in os.environ:
    print("Found supervisor token!!!!")
    super_token = os.environ['SUPERVISOR_TOKEN']


class Api:
    _is_ha_env = False

    def __init__(self) -> None:
        # running on home assistant environment?
        pass
    
    @staticmethod
    def ping():
        headers_auto_config = {
            "Authorization": f'Bearer {super_token}',
            "content-type": "application/json",
        }

        response = None
        try:
            response = requests.get(internal_host, headers=headers_auto_config)
            is_ha_env = True
        except requests.exceptions.ConnectionError as e:
            is_ha_env = False
            logging.error(f"API request failed with Supervisor Token (auto auth)")

        if not is_ha_env:
            headers = {
                "Authorization": 'Bearer ' + token,
                "content-type": "application/json",
            }
            try:
                response = requests.get(url, headers=headers)
            except requests.exceptions.ConnectionError as e:
                logging.error(f"API request failed: cannot connect to Homeassistant API")
                return None

            if response.status_code < 200 or response.status_code > 202:
                logging.error(f"API request failed with personal token: {response.status_code}")
                raise requests.exceptions.ConnectionError("Cannot connect to Homeassistant API")

        return response.text