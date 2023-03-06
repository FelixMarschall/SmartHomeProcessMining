import dash
import pandas as pd

from datetime import date
from dash import Dash, dcc, html, Input, Output, callback
from dash.dependencies import Input, Output
import dash_daq as daq

import page_components.components as components

from homeassistant import Api

dash.register_page(__name__,path="/homesassistant",order=1)

layout = html.Div([
    html.H1('Home Assistant Logbook'),
    dcc.Loading(
            id="loading-2",
            type="circle",
            children=html.Div(id="loading-output-2")
        ),
    html.H3('Filter data'),
    html.Div([
        'Timerange',
        dcc.DatePickerRange(
        id = "logbook-date-picker-range",
        month_format='D-M-Y',
        end_date_placeholder_text='D/M/Y',
        start_date_placeholder_text='D/M/Y',
        clearable=True,
        )
    ]),
    html.Hr(),
    html.Div([
        daq.BooleanSwitch(
        id='delete_update_entries',
        label="Delete Update Entities",
        labelPosition="left",
        on=False),
    ]),
    html.Hr(),
    html.Button('Fetch Logbook', id='fetch-logbook', 
                    style=components.get_button_style()),
    html.Hr(),
    html.Div(id = "fetch_duration"),
    html.Div(id = "quickstats"),
    html.Div(id ="logbook-data", children=[
        html.Div(id="info-field", children='Nothing fetched...'),
    ])
])