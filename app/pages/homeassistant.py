import dash
import pandas as pd

from datetime import date
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from homeassistant import Api


dash.register_page(__name__,path="/homesassistant")

layout = html.Div([
    html.H1('Home Assistant Logbook'),
    html.H3('Filter data'),
    html.Div([
        'Timerange',
        dcc.DatePickerRange(
        month_format='M-D-Y-Q',
        end_date_placeholder_text='M-D-Y-Q',
        start_date_placeholder_text='M-D-Y-Q',
        clearable=True,
        )
    ]),
    html.Div(
        [dcc.Checklist(options=['Delete update. entities'])]
        ),
    html.Hr(),
])