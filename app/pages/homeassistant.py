import dash
import pandas as pd
import dateutil.tz
import time
import logging

from datetime import date
from dash import dcc, html, Input, Output, callback, State
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
        'Dayrange',
        dcc.DatePickerRange(
        id = "logbook-date-picker-range",
        month_format='D-M-Y',
        end_date_placeholder_text='D/M/Y',
        start_date_placeholder_text='D/M/Y',
        clearable=True,
        persistence=True,
        ),
        html.Hr(),
        "Timerange",
        dcc.RangeSlider(0, 24,step=0.01, value=[6, 9], id='time-range-slider', persistence=True, marks=None,
        tooltip={"placement": "bottom", "always_visible": True}),
        html.Div(id='output-container-range-slider'),
        html.Hr(),
        dcc.Checklist(
            options=[
                {'label': 'Monday', 'value': 'Monday'},
                {'label': 'Tuesday', 'value': 'Tuesday'},
                {'label': 'Wednesday', 'value': 'Wednesday'},
                {'label': 'Thursday', 'value': 'Thursday'},
                {'label': 'Friday', 'value': 'Friday'},
                {'label': 'Saturday', 'value': 'Saturday'},
                {'label': 'Sunday', 'value': 'Sunday'}
                ],
            value=['Monday, Tuesday, Wednesday, Thursday, Friday'],
            persistence=True,
            labelStyle={'padding': '5px'},
            id='weekday-checklist'
        )
    ]),
    html.Hr(),
    html.Div([
        daq.BooleanSwitch(
        id='delete_update_entries',
        label="Delete Update Entities",
        labelPosition="top",
        on=True,
        persistence=True,
        style={'display': 'inline-block', 'margin-left': '10px'}),
        daq.BooleanSwitch(
        id='create_help_columns',
        label="Create Helper Columns",
        labelPosition="top",
        on=True,
        persistence=True,
        style={'display': 'inline-block', 'margin-left': '10px'}),
    ],
    ),
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
    State('time-range-slider', 'value'),
    State('weekday-checklist', 'value'),
    State('delete_update_entries', 'on'),
    State('create_help_columns', 'on'),
    prevent_initial_call=False
)
def fetch_logbook(value, start_date, end_date, time_range_slider, weekday_checklist, delete_update_entries, create_help_columns):
    '''Fetches homeassistant logbook and prints in table'''
    logbook = EventData.logbook

    if not logbook is None and value is None:
        # use previous fetch
        quickstats = f"Logbook shape (row, cols): {logbook.shape}"
        return data_components.get_logbook_table(logbook), "locally stored fetch loaded", quickstats, False, False, False, None
        
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

    if status_code != 200:
        logging.error(f"Error fetching logbook, status code: {status_code}")
        return None, None, None, False, False, True, None

    try:
        df = pd.read_json(logbook_data)

        if df.empty:
            logging.error("Empty Logbook fetch, Fetch without start date lists only events from today.")
            return None, None, None, False, True, False, None
    except Exception as e:
        logging.error(e)
        return None, None, None, False, False, True, None
    
    # optimize storage
    #df_json_size = round(df.memory_usage(index=True).sum()/(1000*1000), 2)
    df[df.select_dtypes(['object']).columns] = df.select_dtypes(['object']).apply(lambda x: x.astype('category'))
    df_size = round(df.memory_usage(index=True).sum()/(1000*1000), 2)
    
    # rename dataframe col when to timestamp
    df.rename(columns={"when": "timestamp"}, inplace=True)
    local_tz = dateutil.tz.tzlocal()
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_convert(local_tz)

    # apply timerange filter
    if not (time_range_slider[0]==0 and time_range_slider[1]==24):
        start_hour, start_min = float_to_time(time_range_slider[0])
        end_hour, end_min = float_to_time(time_range_slider[1])

        mask =  (time_range_slider != 0) & (df['timestamp'].dt.time >= pd.to_datetime(f"{start_hour}:{start_min}", format='%H:%M').time()) | \
                (time_range_slider != 24) & (df['timestamp'].dt.time <= pd.to_datetime(f"{end_hour}:{end_min}", format='%H:%M').time())
        df = df.loc[mask]

    # apply weekday filter
    if weekday_checklist:
        df = df[df.timestamp.dt.day_name().isin(weekday_checklist)]

    if delete_update_entries:
        df = df[df.entity_id.str.contains("update.") == False]

    
    # create helper columns
    if create_help_columns:
        df.insert(1, "weekday_H", df["timestamp"].dt.day_name())
        df.insert(2, "single_day_id_H", df["timestamp"].dt.strftime('%Y-%B-%d'))
        df["state"].astype(str).fillna("",inplace=True)
        df.insert(3, "name_state_H", df["entity_id"].astype(str) + "_" + df["state"].astype(str))

    EventData.logbook = df

    quickstats = f"Logbook shape (row, cols): {df.shape}; Panda Framework size: {df_size} MB"

    logging.info(f"Fetched logbook in {end_time_str} with size (row, col) of {df.shape}")
    return data_components.get_logbook_table(df), end_time_str, quickstats, True, False, False, None

@callback(
    Output('output-container-range-slider', 'children'),
    Input('time-range-slider', 'value'))
def update_output(value):
    if value[0] == value[1]:
        return "Select timespan"

    hours1 = int(value[0])
    minutes1 = int(round((value[0] - hours1) * 60))

    hours2 = int(value[1])
    minutes2 = int(round((value[1] - hours2) * 60))

    time1 = f"{hours1:02d}:{minutes1:02d}"
    time2 = f"{hours2:02d}:{minutes2:02d}"

    return f"Time between {time1} and {time2}"

def float_to_time(num):
    hours = int(num)
    minutes = int(round((num - hours) * 60))
    return hours, minutes