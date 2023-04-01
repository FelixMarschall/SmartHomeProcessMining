import os
import logging

# imports for web app
import dash
import dash_bootstrap_components as dbc

# own modules
from homeassistant import Api

# local imports
import page_components.app_components as app_components    

# set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logging.debug(os.environ)
logging.info(f"options.json exists {os.path.isfile('/data/options.json')}")
logging.info(f"Api.ping(): {Api.ping()}")

logging.info("Api.ping():" , Api.ping())

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
    logging.info("Starting dash server...")

    # 

    App.app.run_server(debug=True, host="0.0.0.0")