import os
import requests
import pandas as pd
import logging
import os
import json
from datetime import date

host = "homeassistant.local"
port = 8123

url = f"http://{host}:{port}/api/"

timestamp = "2022-02-15T00:00:00+02:00"

token = "xxxx"

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

# create http headers
headers = {
    "Authorization": f'Bearer {token}',
    "content-type": "application/json",
}


class Api:
    @staticmethod
    def ping():
        """Pings the Homeassistant API"""
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError as e:
            logging.error(
                f"API request failed: cannot connect to Homeassistant API")
            return None

        if response.status_code < 200 or response.status_code > 202:
            logging.error(
                f"API request failed with token: {response.status_code}")

        return response.text

    @staticmethod
    def get_logbook(start: date = None, end_time: date = None):
        """Returns the Logbook"""
        logbook_url = url + "logbook"

        if start is None:
            with requests.get(logbook_url, headers=headers) as r:
                return r.text, r.status_code
        else:
            start = start.strftime('%Y-%m-%d') + "T00%3A00%3A00%2B02%3A00"
            with requests.get(f"{logbook_url}/{start}?end_time=2099-12-31T00%3A00%3A00%2B02%3A00",
                              headers=headers) as r:
                return r.text, r.status_code
