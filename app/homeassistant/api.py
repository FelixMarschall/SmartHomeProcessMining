import requests
import pandas as pd
import logging

internal_host = "http://supervisor/core/api/"
host = "homeassistant.local"
port = 8123
timestamp = "2022-02-15T00:00:00+02:00"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIzMzc5NDBmZmZlNWU0MWJiYmY4MDZmYzYzZmM0MjNhNSIsImlhdCI6MTY3NzcwNjg4MSwiZXhwIjoxOTkzMDY2ODgxfQ.IrgtgxwY1dKjTcNV59ZhX-URvptsQ_MmE6XsPN-23WA"


class Api:
    _is_ha_env = False

    def __init__(self) -> None:
        # running on home assistant environment?
        pass
    
    @staticmethod
    def ping():
        headers_auto_config = {
            "Authorization": 'Bearer ${SUPERVISOR_TOKEN}',
            "content-type": "application/json",
        }

        try:
            response = requests.get(internal_host, headers=headers_auto_config)
            is_ha_env = True
        except requests.exceptions.ConnectionError as e:
            is_ha_env = False
            logging.error(f"API request failed with Supervisor Token (auto auth)")

        if not is_ha_env:
            url = f"http://{host}:{port}/api/"
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

    @staticmethod
    def get_logbook(self):
        '''Returns the logbook'''
        pass    