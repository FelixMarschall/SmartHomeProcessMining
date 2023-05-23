import dash
import pm4py
import time
import logging
import glob
import os

from dash import dcc,html, Input, Output, callback, State, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import pandas as pd
 
from event_data import EventData

import page_components.components as components
import page_components.transformation_components as transformation_components

dash.register_page(__name__,path="/transformation", order=4)

PATH_ASSETS = "./app/assets/"
PATH_IMAGES = PATH_ASSETS + "images/"


layout = html.Div([
    html.H1('Transformation'),
    html.Hr(),
    html.Div(children=[
        html.Div(
        children=[
            'Choose data source',
            dcc.Dropdown(
                id='data-source-dropdown',
                clearable=False,
                style={
                'width': '50%',
                'margin': '10px'
                },
                persistence = True,
            ),
            html.P('Activity column (e.g. "concept:name" or "name_state_id")'),
            dcc.Dropdown(
                id="activity-dropdown",
                clearable=False,
                style={
                'width': '50%',
                'margin': '10px'
                },
                persistence = True,
            ),
            html.P('Case ID column (e.g. "case:concept:name" or "single_day_id_H")'),
            dcc.Dropdown(
                id="case-id-dropdown",
                clearable=False,
                style={
                'width': '50%',
                'margin': '10px'
                },
                persistence = True,
            ),
            html.P('Timestamp column:'),
            dcc.Dropdown(
                id="timestamp-dropdown",
                clearable=False,
                style={
                'width': '50%',
                'margin': '10px'
                },
                persistence = True,
            ),
            ], 
            ),
        ]),
    html.Hr(),
    ### Transformation
    html.Div(children='Choose your favorite algorithmn and set parameters!'),
    dcc.Dropdown(
    ['alpha', 'heuristic', 'inductive'],
    value='inductive',
    clearable=False,
    id='algo-dropdown',
    style={
        'width': '50%',
        'margin': '10px'
    },
    persistence = True
),
    dcc.Loading(
            id="loading-1",
            type="circle",
            children=html.Div(id="loading-output-1")
        ),
    html.H2('Parameters'),
    html.Div(id='alpha-parameters', children="No parameters available for Alpha Miner", hidden=True),
    html.Div(id='inductive-parameters', children=
        [
            html.Label('Noise Threshold', style=transformation_components.get_parameter_input_style()),
            dcc.Input(id='noise_threshold', type='number', min=0.0, max=1.0, step=0.1, value=0.0, persistence=True),
        ],
        hidden=True
    ),
    html.Div(id='heuristic-parameters', children=
        [
            html.Label('Dependency Threshold', style=transformation_components.get_parameter_input_style()),
            dcc.Input(id='dependency_threshold', type='number', min=0.0, max=1.0, step=0.1, value=0.5, persistence=True), #float

            html.Label('AND Threshold', style=transformation_components.get_parameter_input_style()), 
            dcc.Input(id='and_threshold', type='number', min=0.0, max=1.0, step=0.1, value=0.5, persistence=True), #float
            
            html.Label('Loop Two Threshold', style=transformation_components.get_parameter_input_style()),
            dcc.Input(id='loop_two_threshold', type='number', min=0.0, max=1.0, step=0.1, value=0.5, persistence=True), #float

            #html.Label('min act count', style=transformation_components.get_parameter_input_style()),
            #dcc.Input(id='min_act_count', type='number', min=1, step=1, value=1, pattern=u"^[0-9]\d*$", persistence=True), # int

            #html.Label('min dfg occurrences', style=transformation_components.get_parameter_input_style()),
            #dcc.Input(id='min_dfg_occurrences', type='number', min=1, step=1, value=1, pattern=u"^[0-9]\d*$", persistence=True), # int
        ],
        hidden=True
    ),
    html.Hr(),

    html.Button('Start mining', id='mine-button', 
                    style=components.get_button_style()),
    html.Div(id='mining-duration'),
    dbc.Alert(
            "Success!",
            id="alert-mining-succ",
            is_open=False,
            duration=6000,
            color="success"
            ),
    dbc.Alert(
            "Mining failed!",
            id="alert-mining-error",
            is_open=False,
            duration=16000,
            color="danger"
            ),
    html.Div(id='graphs',
             children=[
                html.Hr(),
                html.H2('Directly-follows graph'),
                dbc.Button(
                    "Collapse/Expand",
                    id="collapse-button",
                    className="me-1",
                    color="secondary",
                    n_clicks=0
                ),
                dbc.Collapse(
                    [html.P("Graph is not influenced by the transformation algorithm or the parameters above."),
                    html.Img(id= "dfg", alt="DfG Image", style={'width':'100%'}),],
                id="collapse",
                is_open=True,
                ),   
                html.Hr(),
                html.H2('Petri Net'),
                html.Img(id= "petrinet", alt="Petri Net Image", style={'width':'100%'}),
                html.Hr(),
                html.H2('BPMN Graph'),
                html.Img(id= "bpmn", alt="BPMN Image", style={'width':'100%'}),
                html.Hr(),
                html.H2('Process Tree'),
                html.Img(id= "processtree", alt="Process Tree", style={'width':'100%'}),
                html.Hr(),
    ]
    ),
])

@callback(
    Output("data-source-dropdown", "options"),
    Output("activity-dropdown", "options"),
    Output("case-id-dropdown", "options"),
    Output("timestamp-dropdown", "options"),
    Input("data-source-dropdown", "value"),
    prevent_initial_call=False
)
def update_datasource_dropdown(data_source):
    # check if data is available
    options = []
    logbook_is_available = EventData.logbook is not None
    uploaded_log_is_available = EventData.uploaded_log is not None

    options = [
            {"label": "Uploaded Event Log","value": "uploaded_log", "disabled": not uploaded_log_is_available},
            {"label": "Home Assistant","value": "home-assistant", "disabled": not logbook_is_available},
            {"label": "Example Logbook","value": "example"},
            ]
        
    if data_source == "home-assistant" and logbook_is_available:
        activity_options = list(EventData.logbook.columns)
        case_id_options = list(EventData.logbook.columns)
        timestamp_options = list(EventData.logbook.columns)
    elif data_source == "uploaded_log" and uploaded_log_is_available:
        activity_options = list(EventData.uploaded_log.columns)
        case_id_options = list(EventData.uploaded_log.columns)
        timestamp_options = list(EventData.uploaded_log.columns)
    elif data_source == "example":
        activity_options = list(EventData.example_log.columns)
        case_id_options = list(EventData.example_log.columns)
        timestamp_options = list(EventData.example_log.columns)
    else:
        return options, no_update, no_update, no_update

    return options, activity_options, case_id_options, timestamp_options


### Hide/Show Parameters for Transformation Algorithms
@callback(
    Output('alpha-parameters', 'hidden'),
    Output('heuristic-parameters', 'hidden'),
    Output('inductive-parameters', 'hidden'),
    Input('algo-dropdown', 'value'),
    prevent_initial_call=False)
def update_parameters_visibility(algo):
    """Calles when dropdown for transformation algorithm is changed."""

    if algo == "alpha":
        return False, True, True
    elif algo == "inductive":
        return True, True, False
    elif algo == "heuristic":
        return True, False, True
    else:
        raise PreventUpdate("Visibility did not change.")

### Transformation "start mining" Button
@callback(
    Output('mining-duration', 'children'),
    Output('alert-mining-succ', 'is_open'),
    Output('alert-mining-error', 'is_open'),
    Output('image_file_name', 'data'),
    Output('loading-1', 'children'),
    Input('mine-button', 'n_clicks'),
    State('algo-dropdown', 'value'),
    State('data-source-dropdown', 'value'),
    # inductive algo
    State('noise_threshold', 'value'),
    # heuristc algo
    State('dependency_threshold', 'value'), #float
    State('and_threshold', 'value'), #float
    State('loop_two_threshold', 'value'), #int
    # mining columns
    State('activity-dropdown', 'value'),
    State('case-id-dropdown', 'value'),
    State('timestamp-dropdown', 'value'),
    prevent_initial_call=True
)
def update_transformation(value, algo, data_source, noise_threshold, dependency_threshold, and_threshold, loop_two_threshold, activity, case_id, timestamp):
    """Calles when transformation button is clicked."""
    logging.debug(f"Callback 'start mining' button with value: {value} and algo: {algo}")

    if value is None:
        raise PreventUpdate("Nothing clicked")

    if data_source == "home-assistant":
        logbook_temp = EventData.logbook
    else:
        logbook_temp = EventData.uploaded_log

    if logbook_temp is None:
        logbook_temp = EventData.example_log

    logbook_temp[timestamp] = pd.to_datetime(logbook_temp[timestamp])

    start_time = time.perf_counter()
    try:
        dfg, sa, ea = pm4py.discover_dfg(logbook_temp, activity_key=activity, case_id_key=case_id, timestamp_key=timestamp)
        if algo == "alpha":
            process_model, start, end = pm4py.discover_petri_net_alpha(
                log=logbook_temp,
                activity_key=activity,
                timestamp_key=timestamp,
                case_id_key=case_id)
        elif algo == "inductive":
            if noise_threshold is None or noise_threshold > 1 or noise_threshold < 0:
                noise_threshold = 0.0
                logging.debug("Noise threshold is not set or not in range [0,1], using default value 0.0")

            process_model, start, end = pm4py.discover_petri_net_inductive(
                log=logbook_temp,
                noise_threshold=noise_threshold,
                activity_key=activity,
                timestamp_key=timestamp,
                case_id_key=case_id
                )
        elif algo == "heuristic":
            # check values and set to pm4py default values if not in range [0,1]
            if dependency_threshold is None or dependency_threshold > 1 or dependency_threshold < 0:
                dependency_threshold = 0.5
            if and_threshold is None or and_threshold > 1 or and_threshold < 0:
                and_threshold = 0.65
            if loop_two_threshold is None or loop_two_threshold > 1 or loop_two_threshold < 0:
                loop_two_threshold = 0.5
            
            process_model, start, end = pm4py.discover_petri_net_heuristics(
                log=logbook_temp,
                dependency_threshold=dependency_threshold,
                and_threshold=and_threshold,
                loop_two_threshold=loop_two_threshold,
                activity_key=activity,
                timestamp_key=timestamp,
                case_id_key=case_id
                )
        else:
            logging.error("Algorithm is not chosen")
            return no_update, False, True, no_update, no_update
    except ConnectionError as e:
        logging.error(f"Mining went wrong: {e}")
        return no_update, False, True, no_update, no_update

    mining_duration = time.perf_counter() - start_time
    mining_duration = "mining duration: "+ str(round(mining_duration,2)) + "s"
    logging.info(f"[{algo}] {mining_duration}")

    bpmn = pm4py.convert_to_bpmn(process_model, start, end)

    try:
        pt = pm4py.convert_to_process_tree(process_model, start, end)
    except Exception as e:
        pt = None
        logging.error(type(e).__name__ + " converting process model to process tree: " + str(e))

    timestr = time.strftime("%Y%m%d-%H%M%S")

    dfg_file_name = f"dfg_{timestr}.svg"
    pn_file_name = f"pn_{timestr}.svg"
    bpmn_file_name = f"bpmn_{timestr}.svg"
    pt_file_name = f"pt_{timestr}.svg"

    dfg_file_path = PATH_ASSETS + dfg_file_name
    pn_file_path = PATH_ASSETS + pn_file_name
    bpmn_file_path = PATH_ASSETS + bpmn_file_name
    pt_file_path = PATH_ASSETS + pt_file_name

    # delete all images in assets
    files = glob.glob(PATH_ASSETS +'*')
    for i in files:
        if ".png" in i or ".svg" in i:
            os.remove(i)

    try:
        # safe image to disk
        pm4py.save_vis_dfg(dfg, sa, ea, dfg_file_path)
        pm4py.save_vis_petri_net(process_model, start, end, pn_file_path)
        pm4py.save_vis_bpmn(bpmn, bpmn_file_path)

        if pt is not None:
            pm4py.save_vis_process_tree(pt, pt_file_path)
    except Exception as e:
        logging.error(type(e).__name__ + " while saving process model: " + str(e))

        return no_update, False, True, no_update, no_update

    image_file_name = {
        "algorithm": algo,
        "dfg": dfg_file_name,
        "petri": pn_file_name,
        "bpmn": bpmn_file_name,
        "tree": pt_file_name
    }
    
    return mining_duration, True, False, image_file_name, None

@callback(
    Output('dfg', 'src'),
    Output('petrinet','src'), 
    Output('bpmn','src'),
    Output('processtree','src'),
    Input('image_file_name' ,'modified_timestamp'),
    State('image_file_name', 'data'),
)
def update_graphs(ts, image_file_name):
    '''Changes the graph image when image data changed'''
    logging.info("process models path",image_file_name)

    if image_file_name is None:
        raise PreventUpdate()
    
    return dash.get_asset_url(image_file_name["dfg"]),dash.get_asset_url(image_file_name["petri"]),dash.get_asset_url(image_file_name["bpmn"]),dash.get_asset_url(image_file_name["tree"])

@callback(
    Output("collapse", "is_open"),
    Input("collapse-button", "n_clicks"),
    State("collapse", "is_open"),
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open