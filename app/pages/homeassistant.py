import dash
import pandas as pd
import dateutil.tz
import time
import logging

from datetime import date
from dash import dcc, html, Input, Output, callback, State, ctx
from dash.dependencies import Input, Output
import dash_daq as daq
import dash_bootstrap_components as dbc

import page_components.data_components as data_components
import page_components.components as components

from homeassistant import Api
from event_data import EventData

dash.register_page(__name__, path="/homesassistant", order=1)

layout = html.Div(
    [
        html.H1("Home Assistant Logbook"),
        html.Hr(),
        dcc.Loading(
            id="loading-2", type="circle", children=html.Div(id="loading-output-2")
        ),
        html.H3("Filter data"),
        html.Div(
            [
                "Dayrange",
                dcc.DatePickerRange(
                    id="logbook-date-picker-range",
                    month_format="D-M-Y",
                    end_date_placeholder_text="D/M/Y",
                    start_date_placeholder_text="D/M/Y",
                    clearable=True,
                    persistence=True,
                ),
                html.Hr(),
                "Timerange",
                dcc.RangeSlider(
                    0,
                    24,
                    step=0.01,
                    value=[6, 9],
                    id="time-range-slider",
                    persistence=True,
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
                html.Div(id="output-container-range-slider"),
                html.Hr(),
                dcc.Checklist(
                    options=[
                        {"label": "Monday", "value": "Monday"},
                        {"label": "Tuesday", "value": "Tuesday"},
                        {"label": "Wednesday", "value": "Wednesday"},
                        {"label": "Thursday", "value": "Thursday"},
                        {"label": "Friday", "value": "Friday"},
                        {"label": "Saturday", "value": "Saturday"},
                        {"label": "Sunday", "value": "Sunday"},
                    ],
                    value=["Monday, Tuesday, Wednesday, Thursday, Friday"],
                    persistence=True,
                    labelStyle={"padding": "5px"},
                    id="weekday-checklist",
                ),
            ]
        ),
        html.Hr(),
        html.Div(
            [
                daq.BooleanSwitch(
                    id="delete_update_entries",
                    label="Delete Update Entities",
                    labelPosition="top",
                    on=True,
                    persistence=True,
                    style={"display": "inline-block", "margin-left": "10px"},
                ),
                daq.BooleanSwitch(
                    id="create_help_columns",
                    label="Create Helper Columns",
                    labelPosition="top",
                    on=True,
                    persistence=True,
                    style={"display": "inline-block", "margin-left": "10px"},
                ),
            ],
        ),
        html.Hr(),
        html.Button(
            "Fetch Logbook", id="fetch-logbook", style=components.get_button_style()
        ),
        html.Hr(),
        dbc.Alert(
            "Fetch was successfull!",
            id="alert-fetch-succ",
            is_open=False,
            duration=6000,
            color="success",
        ),
        dbc.Alert(
            "Fetch is empty, set an earlier start date!",
            id="alert-fetch-fail",
            is_open=False,
            duration=8000,
            color="warning",
        ),
        dbc.Alert(
            "No connection to Home Assistant possible!",
            id="alert-fetch-error",
            is_open=False,
            duration=16000,
            color="danger",
        ),
        html.Div(id="fetch_duration"),
        html.Div(id="quickstats"),
        html.Div(
            id="logbook-data",
            children=[
                html.Div(id="info-field", children="Nothing fetched..."),
            ],
        ),
        html.Hr(),
        ### Filter entities ###
        html.H3("Filter entities"),
        html.Div(
            children=[
                "Choose entities which should be included (Filter function)",
                html.Br(),
                # daq.BooleanSwitch(
                # id='is_filter_entities',
                # label="Filter entities",
                # labelPosition="top",
                # on=True,
                # persistence=True,
                # style={'display': 'inline-block', 'margin-left': '15px'},
                # ),
                dbc.Button(
                    "ALL",
                    id="all-button",
                    color="primary",
                    className="me-1",
                ),
                dbc.Button(
                    "INVERT",
                    id="invert-selection-button",
                    color="primary",
                    className="me-1",
                    outline=True,
                ),
                dbc.Button(
                    "Invert automation",
                    id="select-automations-button",
                    color="primary",
                    className="me-1",
                    outline=True,
                ),
                dbc.Button(
                    "Invert sensor",
                    id="select-sensor-button",
                    color="primary",
                    className="me-1",
                    outline=True,
                ),
                dbc.Button(
                    "Invert binary",
                    id="select-binary-button",
                    color="primary",
                    className="me-1",
                    outline=True,
                ),
                dbc.Button(
                    "Invert switch",
                    id="select-switch-button",
                    color="primary",
                    className="me-1",
                    outline=True,
                ),
                dbc.Button(
                    "Invert sun",
                    id="select-sun-button",
                    color="primary",
                    className="me-1",
                    outline=True,
                ),
                html.Br(),
                dcc.Checklist(
                    id="entities-checklist",
                    labelStyle={"margin": "10px"},
                    persistence=True,
                    options=[],
                ),
                html.Br(),
                html.Button(
                    "Filter", id="filter-entities", style=components.get_button_style()
                ),
            ]
        ),
    ]
)


@callback(
    Output("logbook-data", "children", allow_duplicate=True),
    Output("fetch_duration", "children", allow_duplicate=True),
    Output("quickstats", "children", allow_duplicate=True),
    Output("alert-fetch-succ", "is_open"),
    Output("alert-fetch-fail", "is_open"),
    Output("alert-fetch-error", "is_open"),
    Output("loading-2", "children"),
    Input("fetch-logbook", "n_clicks"),
    State("logbook-date-picker-range", "start_date"),
    State("logbook-date-picker-range", "end_date"),
    State("time-range-slider", "value"),
    State("weekday-checklist", "value"),
    State("delete_update_entries", "on"),
    State("create_help_columns", "on"),
    prevent_initial_call="initial_duplicate",
)
def fetch_logbook(
    value,
    start_date,
    end_date,
    time_range_slider,
    weekday_checklist,
    delete_update_entries,
    create_help_columns,
):
    """Fetches homeassistant logbook and prints in table"""
    logbook = EventData.logbook

    if not logbook is None and value is None:
        # use previous fetch
        quickstats = f"Logbook shape (row, cols): {logbook.shape}"
        return (
            data_components.get_logbook_table(logbook),
            "locally stored fetch loaded",
            quickstats,
            False,
            False,
            False,
            None,
        )

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
            logging.error(
                "Empty Logbook fetch, Fetch without start date lists only events from today."
            )
            return None, None, None, False, True, False, None
    except Exception as e:
        logging.error(e)
        return None, None, None, False, False, True, None

    # optimize storage
    # df_json_size = round(df.memory_usage(index=True).sum()/(1000*1000), 2)
    df[df.select_dtypes(["object"]).columns] = df.select_dtypes(["object"]).apply(
        lambda x: x.astype("category")
    )
    df_size = round(df.memory_usage(index=True).sum() / (1000 * 1000), 2)

    # rename dataframe col when to timestamp
    df.rename(columns={"when": "timestamp"}, inplace=True)
    local_tz = dateutil.tz.tzlocal()
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.tz_convert(local_tz)

    # apply timerange filter
    if not (time_range_slider[0] == 0 and time_range_slider[1] == 24):
        start_hour, start_min = float_to_time(time_range_slider[0])
        end_hour, end_min = float_to_time(time_range_slider[1])

        mask = (time_range_slider != 0) & (
            df["timestamp"].dt.time
            >= pd.to_datetime(f"{start_hour}:{start_min}", format="%H:%M").time()
        ) | (time_range_slider != 24) & (
            df["timestamp"].dt.time
            <= pd.to_datetime(f"{end_hour}:{end_min}", format="%H:%M").time()
        )
        df = df.loc[mask]

    # apply weekday filter
    if weekday_checklist:
        df = df[df.timestamp.dt.day_name().isin(weekday_checklist)]

    if delete_update_entries:
        df = df[df.entity_id.str.contains("update.") == False]

    # create helper columns
    if create_help_columns:
        df.insert(1, "weekday_H", df["timestamp"].dt.day_name())
        df.insert(2, "single_day_id_H", df["timestamp"].dt.strftime("%Y-%B-%d"))
        df["state"].astype(str).fillna("", inplace=True)
        df.insert(
            3,
            "name_state_H",
            df["entity_id"].astype(str) + "_" + df["state"].astype(str),
        )

    EventData.logbook = df
    EventData.logbook_unfiltered = df

    quickstats = (
        f"Logbook shape (row, cols): {df.shape}; Panda Framework size: {df_size} MB"
    )

    logging.info(
        f"Fetched logbook in {end_time_str} with size (row, col) of {df.shape}"
    )
    return (
        data_components.get_logbook_table(df),
        end_time_str,
        quickstats,
        True,
        False,
        False,
        None,
    )


@callback(
    Output("entities-checklist", "options"),
    Output("entities-checklist", "value"),
    Input("logbook-data", "children"),
    State("entities-checklist", "value"),
    prevent_initial_call=True,
)
def update_entities_checklist(data, checklist_value):
    """Updates checklist with all entities from logbook"""
    logging.info("Updating entities checklist")
    if EventData.logbook_unfiltered is None:
        return []

    entities = EventData.logbook_unfiltered["entity_id"].unique()
    if checklist_value is None:
        return [{"label": entity, "value": entity} for entity in entities], entities

    return [{"label": entity, "value": entity} for entity in entities], checklist_value


@callback(
    Output("logbook-data", "children"),
    Output("quickstats", "children"),
    Output("fetch_duration", "children"),
    Input("filter-entities", "n_clicks"),
    State("entities-checklist", "value"),
    prevent_initial_call=True,
)
def filter_entities(n_clicks, entities):
    """Filters logbook for selected entities"""
    if EventData.logbook_unfiltered is None:
        return dash.no_update

    if entities is None:
        logging.info("No entities selected")
        return dash.no_update

    logging.info(f"Filtering logbook for entities: {entities}")
    df = EventData.logbook_unfiltered[
        EventData.logbook_unfiltered["entity_id"].isin(entities)
    ]

    df_size = round(df.memory_usage(index=True).sum() / (1000 * 1000), 2)
    quickstats = (
        f"Logbook shape (row, cols): {df.shape}; Panda Framework size: {df_size} MB"
    )

    return data_components.get_logbook_table(df), quickstats, None


@callback(
    Output("entities-checklist", "value", allow_duplicate=True),
    Input("all-button", "n_clicks"),
    Input("invert-selection-button", "n_clicks"),
    Input("select-automations-button", "n_clicks"),
    Input("select-sensor-button", "n_clicks"),
    Input("select-binary-button", "n_clicks"),
    Input("select-switch-button", "n_clicks"),
    Input("select-sun-button", "n_clicks"),
    State("entities-checklist", "value"),
    prevent_initial_call=True,
)
def invert_selection(all, invert, automation, sensor, binary, switch, sun, entities):
    """Inverts selection of entities"""
    if EventData.logbook_unfiltered is None:
        return dash.no_update

    if entities is None:
        logging.info("No entities selected")
        return dash.no_update

    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    all_entities = EventData.logbook_unfiltered["entity_id"].unique()
    if button_id == "all-button":
        if entities:
            return []
        else:
            return all_entities
    elif button_id == "select-automations-button":
        prefix = "automation"
    elif button_id == "select-sensor-button":
        prefix = "sensor"
    elif button_id == "select-binary-button":
        prefix = "binary"
    elif button_id == "select-switch-button":
        prefix = "switch"
    elif button_id == "select-sun-button":
        prefix = "sun"
    else:
        # invert button
        inverted_entities = list(set(all_entities) - set(entities))
        return inverted_entities

    subset = [entity for entity in all_entities if entity.startswith(prefix)]
    if any(entity.startswith(prefix) for entity in entities):
        entities = list(set(entities) - set(subset))
    else:
        entities = list(set(entities) | set(subset))
    return entities


@callback(
    Output("output-container-range-slider", "children"),
    Input("time-range-slider", "value"),
)
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
