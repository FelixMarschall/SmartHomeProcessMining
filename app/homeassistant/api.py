import requests
import pandas as pd
import logging
import os
import json

host = "homeassistant.local"
port = 8123
internal_host = "http://supervisor/core/api/"
url = f"http://{host}:{port}/api/"

timestamp = "2022-02-15T00:00:00+02:00"


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIzMzc5NDBmZmZlNWU0MWJiYmY4MDZmYzYzZmM0MjNhNSIsImlhdCI6MTY3NzcwNjg4MSwiZXhwIjoxOTkzMDY2ODgxfQ.IrgtgxwY1dKjTcNV59ZhX-URvptsQ_MmE6XsPN-23WA"

if  os.path.isfile("/data/options.json"):
    with open('/data/options.json') as json_file:
        options_config = json.load(json_file)
        if len(options_config['credential_secret']) >= 10:
            token = options_config['credential_secret'] 
            print("Individual token setted.")



super_token = None
if 'SUPERVISOR_TOKEN' in os.environ:
    print("Found supervisor token!!!!")
    super_token = os.environ['SUPERVISOR_TOKEN']


class Api:
    def __init__(self) -> None:
        # running on home assistant environment?
        pass
    
    @staticmethod
    def ping():
        if not super_token is None: 
            headers_auto_config = {
                "Authorization": f'Bearer {super_token}',
                "content-type": "application/json",
            }

            response = None
            try:
                response = requests.get(internal_host, headers=headers_auto_config)
            except requests.exceptions.ConnectionError as e:
                logging.error(f"API request failed with Supervisor Token (auto auth)")
        else:
            headers = {
                "Authorization": f'Bearer {token}',
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
    def get_logbook(start, end_time = "2099-12-31T00%3A00%3A00%2B02%3A00"):
        header = None
        if super_token is None:
            header = headers = {
                "Authorization": f'Bearer {token}',
                "content-type": "application/json",
            }
        else:
            header = {
                "Authorization": f'Bearer {super_token}',
                "content-type": "application/json",
            }

        url_timestamp = f"http://{host}:{port}/api/logbook/{timestamp}?end_time=2099-12-31T00%3A00%3A00%2B02%3A00"
