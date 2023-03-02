import requests
import pandas as pd
import logging


internal_host = "http://supervisor/core/api/"
host = "homeassistant.local"
port = 8123
timestamp = "2022-02-15T00:00:00+02:00"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIzMzc5NDBmZmZlNWU0MWJiYmY4MDZmYzYzZmM0MjNhNSIsImlhdCI6MTY3NzcwNjg4MSwiZXhwIjoxOTkzMDY2ODgxfQ.IrgtgxwY1dKjTcNV59ZhX-URvptsQ_MmE6XsPN-23WA"


class Api:
    is_ha_env = False

    def __init__(self) -> None:
        # running on home assistant environment?
        pass
    
    def ping(self):
        headers_auto_config = {
            "Authorization": 'Bearer ${SUPERVISOR_TOKEN}',
            "content-type": "application/json",
        }

        global is_ha_env
        try:
            response = requests.get(internal_host, headers=headers_auto_config)
            is_ha_env = True
        except requests.exceptions.ConnectionError as e:
            is_ha_env = False
            logging.error(f"API Logbook request failed with Supervisor Token (auto auth)")

        if not is_ha_env:
            url = f"http://{host}:{port}/api/"
            headers = {
                "Authorization": 'Bearer ' + token,
                "content-type": "application/json",
            }
            response = requests.get(url, headers=headers)

            if response.status_code < 200 or response.status_code > 202:
                logging.error(f"API Logbook request failed with personal token: {response.status_code}")
                raise requests.exceptions.ConnectionError("Cannot connect to Homeassistant API")
        return response.text

    def get_logbook(self):
        '''Returns the logbook'''
        pass    