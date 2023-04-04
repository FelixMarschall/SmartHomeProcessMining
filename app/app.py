import os
import logging

# imports for web app
import dash
import dash_bootstrap_components as dbc

# own modules
from homeassistant import Api

# local imports
import page_components.app_components as app_components    


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
        return App.__conf.get(name)

if __name__ == "__main__":
    logging.info("Starting App...")

    # print home assistant environment variables
    logging.debug(os.environ)
    logging.debug(f"options.json exists {os.path.isfile('/data/options.json')}")

    # test if home assistant is reachable
    logging.info("Test connection to Home Assistant...")
    logging.info(f"Api.ping(): {Api.ping()}")

    # remove old uploaded log
    if os.path.isfile('app/assets/temp/uploaded.csv'):
        os.remove('app/assets/temp/uploaded.csv')
    if os.path.isfile('app/assets/temp/uploaded.xes'):
        os.remove('app/assets/temp/uploaded.xes')
    if os.path.isfile('app/assets/temp/uploaded.feather'):
        os.remove('app/assets/temp/uploaded.feather')

    logging.info("Starting dash server...")
    App.app.run_server(debug=True, host="0.0.0.0")