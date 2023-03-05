import dash
import pandas as pd

from datetime import date
from dash import Dash, dcc, html, Input, Output, callback
from dash.dependencies import Input, Output

import page_components.components as components

from homeassistant import Api

dash.register_page(__name__,path="/homesassistant",order=1)

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
    html.Button('Fetch Logbook', id='fetch-logbook', 
                    style=components.get_button_style()),
    html.Hr(),
    html.Div(id ="logbook-data", children=[
        html.Div(id="info-field", children='Nothing fetched...'),
    ])
])