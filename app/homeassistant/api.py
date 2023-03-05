import requests
import pandas as pd
import logging
import os
import json

host = "homeassistant.local"
port = 8123

url = f"http://{host}:{port}/api/"

timestamp = "2022-02-15T00:00:00+02:00"

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIzMzc5NDBmZmZlNWU0MWJiYmY4MDZmYzYzZmM0MjNhNSIsImlhdCI6MTY3NzcwNjg4MSwiZXhwIjoxOTkzMDY2ODgxfQ.IrgtgxwY1dKjTcNV59ZhX-URvptsQ_MmE6XsPN-23WA"

# check if key store in options (Homeassistant)
if os.path.isfile("/data/options.json"):
    with open('/data/options.json') as json_file:
        options_config = json.load(json_file)
        if len(options_config['credential_secret']) >= 10:
            token = options_config['credential_secret']
            print("Individual token setted.")

# check if key stored in environment variables
has_os_token = False
if 'SUPERVISOR_TOKEN' in os.environ:
    print("Found supervisor token!!!!")
    has_os_token = True
    url = "http://supervisor/core/api/"
    token = os.environ['SUPERVISOR_TOKEN']

logbook_url = url + "logbook"

# create http headers
headers = {
    "Authorization": f'Bearer {token}',
    "content-type": "application/json",
}


class Api:

    @staticmethod
    def ping():
        response = None
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError as e:
            logging.error(f"API request failed: cannot connect to Homeassistant API")
            return None

        if response.status_code < 200 or response.status_code > 202:
            logging.error(f"API request failed with token: {response.status_code}")

        return response.text

    @staticmethod
    def get_logbook(start=None, end_time="2099-12-31T00%3A00%3A00%2B02%3A00"):
        if start is None:
            with requests.get(logbook_url, headers=headers) as r:
                return r.text, r.status_code
        else:
            with requests.get(f"{logbook_url}{timestamp}?end_time=2099-12-31T00%3A00%3A00%2B02%3A00",
                              headers=headers) as r:
                return r.text, r.status_code
