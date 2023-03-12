import os
import logging
from datetime import date

# imports for web app
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd

# own modules
from homeassistant import Api

# process mining imports
import pm4py

# local imports
import page_components.data_components as data_components
import page_components.app_components as app_components
import page_components.transformation_components as transformation_components
    

# set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logging.debug(os.environ)
logging.info(f"options.json exists {os.path.isfile('/data/options.json')}")
logging.info(f"Api.ping(): {Api.ping()}")

print("Api.ping():" , Api.ping())

class App:
    # do not change
    __conf = {
        "PATH_ASSETS": "./app/assets/",
        "PATH_IMAGES": "./app/assets/images/"
    }
    
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
    app.layout = app_components.get_layout()

    @staticmethod
    def config(name):
        return App.__conf[name]

if __name__ == "__main__":
    logging.info("Starting dash server...")
    App.app.run_server(debug=False, host="0.0.0.0")