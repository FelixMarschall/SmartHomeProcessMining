import dash
import pandas as pd
import time
import logging

from datetime import date
from dash import Dash, dcc, html, Input, Output, callback, State
from dash.dependencies import Input, Output
import dash_daq as daq
import dash_bootstrap_components as dbc

import page_components.data_components as data_components
import page_components.components as components

from homeassistant import Api
from event_data import EventData

dash.register_page(__name__,path="/homesassistant",order=1)

layout = html.Div([
    html.H1('Home Assistant Logbook'),
    html.Hr(),
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
        labelPosition="top",
        on=False),
    ]),
    html.Hr(),
    html.Button('Fetch Logbook', id='fetch-logbook', 
                    style=components.get_button_style()),
    html.Hr(),
    dbc.Alert(
            "Fetch was successfull!",
            id="alert-fetch-succ",
            is_open=False,
            duration=6000,
            color="success"
            ),
    dbc.Alert(
            "Fetch is empty, set an earlier start date!",
            id="alert-fetch-fail",
            is_open=False,
            duration=8000,
            color="warning"
            ),
    dbc.Alert(
            "No connection to Home Assistant possible!",
            id="alert-fetch-error",
            is_open=False,
            duration=16000,
            color="danger"
            ),
    html.Div(id = "fetch_duration"),
    html.Div(id = "quickstats"),
    html.Div(id ="logbook-data", children=[
        html.Div(id="info-field", children='Nothing fetched...'),
    ])
])

@callback(
    Output("logbook-data", "children"),
    Output("fetch_duration", "children"),
    Output("quickstats", "children"),
    Output("alert-fetch-succ","is_open"),
    Output("alert-fetch-fail","is_open"),
    Output("alert-fetch-error","is_open"),
    Output('loading-2', 'children'),
    Input("fetch-logbook", "n_clicks"),
    State('logbook-date-picker-range', 'start_date'),
    State('logbook-date-picker-range', 'end_date'),
    State('delete_update_entries', 'on'),
    prevent_initial_call=False
)
def fetch_logbook(value, start_date, end_date, delete_update_entries):
    '''Fetches homeassistant logbook and prints in table'''
    logbook = EventData.logbook

    if not logbook is None and value is None:
        # use previous fetch
        quickstats = f"Logbook shape (row, cols): {logbook.shape}"
        return data_components.get_logbook_table(logbook), "locally stored fetch loaded", quickstats, False, False, False, None

    logbook_data = None
    status_code = None
    
    start_time = time.perf_counter()
    try:
        if start_date is not None:
            start_date_object = date.fromisoformat(start_date)
            logbook_data, status_code = Api.get_logbook(start_date_object)
        else:
            logbook_data, status_code = Api.get_logbook()
    except Exception as e:
        logging.error(e)
        return None, None, None, False, False, True, None


    end_time = round(time.perf_counter() - start_time, 2)
    end_time_str = f"{end_time} seconds"

    # if end_date is not None:
    #     end_date_object = date.fromisoformat(end_date)
    #     end_date_string = end_date_object.strftime('%B %d, %Y')

    df = pd.read_json(logbook_data)

    if df.empty:
        logging.error("Empty Logbook fetch, Fetch without start date lists only events from today.")
        return None, None, None, False, True, False, None

    
    # optimize storage
    df_json_size = round(df.memory_usage(index=True).sum()/(1000*1000), 2)
    df[df.select_dtypes(['object']).columns] = df.select_dtypes(['object']).apply(lambda x: x.astype('category'))
    df_size = round(df.memory_usage(index=True).sum()/(1000*1000), 2)
    
    if delete_update_entries:
        df = df[df.entity_id.str.contains("update.") == False]

    EventData.logbook = df

    quickstats = f"Logbook shape (row, cols): {df.shape}; Panda Framework size: {df_size}"

    logging.info(f"Fetched logbook in {end_time_str} with size (row, col) of {df.shape}")
    return data_components.get_logbook_table(df), end_time_str, quickstats, True, False, False, None