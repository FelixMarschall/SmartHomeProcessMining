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
    ### Transformation
    html.Div(children='Choose your favorite algorithmn and set parameters!'),
    dcc.Dropdown(
    ['alpha', 'heuristic', 'inductive'],
    value='alpha',
    clearable=False,
    id='algo-dropdown',
    style={
        'width': '50%',
        'margin': '10px'
    }),
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
            dcc.Input(id='noise_threshold', type='number', min=0.0, max=1.0, step=0.1, value=0.0),
        ],
        hidden=True
    ),
    html.Div(id='heuristic-parameters', children=
        [
            html.Label('Dependency Threshold', style=transformation_components.get_parameter_input_style()),
            dcc.Input(id='dependency_threshold', type='number', min=0.0, max=1.0, step=0.1, value=0.5), #float

            html.Label('AND Threshold', style=transformation_components.get_parameter_input_style()), 
            dcc.Input(id='and_threshold', type='number', min=0.0, max=1.0, step=0.1, value=0.5), #float
            
            html.Label('Loop Two Threshold', style=transformation_components.get_parameter_input_style()),
            dcc.Input(id='loop_two_threshold', type='number', min=0.0, max=1.0, step=0.1, value=0.5), #float

            html.Label('min act count', style=transformation_components.get_parameter_input_style()),
            dcc.Input(id='min_act_count', type='number', min=1, step=1, value=1, pattern=u"^[0-9]\d*$"), # int

            html.Label('min dfg occurrences', style=transformation_components.get_parameter_input_style()),
            dcc.Input(id='min_dfg_occurrences', type='number', min=1, step=1, value=1, pattern=u"^[0-9]\d*$"), # int
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
                html.H2('Petri Net'),
                html.Img(id= "petrinet", src=dash.get_asset_url("pn.svg"), alt="Petri Net Image", style={'width':'100%'}),
                html.Hr(),
                html.H2('BPMN Graph'),
                html.Img(id= "bpmn", src=dash.get_asset_url("bpmn.svg"), alt="BPMN Image", style={'width':'100%'}),
                html.Hr(),
                html.H2('Process Tree'),
                html.Img(id= "processtree", src=dash.get_asset_url("pt.svg"), alt="Process Tree", style={'width':'100%'}),
                html.Hr(),
    ]
    ),
])


### Hide/Show Parameters for Transformation Algorithms
@callback(
    Output('alpha-parameters', 'hidden'),
    Output('heuristic-parameters', 'hidden'),
    Output('inductive-parameters', 'hidden'),
    Input('algo-dropdown', 'value'),
    prevent_initial_call=True)
def update_parameters_visibility(algo):
    """Calles when dropdown for transformation algorithm is changed."""

    if algo == "alpha":
        return False, True, True
    elif algo == "inductive":
        return True, False, True
    elif algo == "heuristic":
        return True, True, False
    else:
        raise PreventUpdate("Visibility did not change.")

### Transformation "start mining" Button
@callback(
    Output('petrinet','src'),
    Output('bpmn','src'),
    Output('processtree','src'),
    Output('mining-duration', 'children'),
    Output('alert-mining-succ', 'is_open'),
    Output('alert-mining-error', 'is_open'),
    Output('loading-1', 'children'),
    #Output('graphs', 'children'),
    Input('mine-button', 'n_clicks'),
    State('algo-dropdown', 'value'),
    # inductive algo
    State('noise_threshold', 'value'),
    # heuristc algo
    State('dependency_threshold', 'value'), #float
    State('and_threshold', 'value'), #float
    State('loop_two_threshold', 'value'), #int
    State('min_act_count', 'value'), #int
    State('min_dfg_occurrences', 'value'), #int
    prevent_initial_call=True
)
def update_transformation(value, algo, noise_threshold, dependency_threshold, and_threshold, loop_two_threshold, min_act_count, min_dfg_occurrences):
    """Calles when transformation button is clicked."""
    logging.debug(f"Callback 'start mining' button with value: {value} and algo: {algo}")

    if EventData.uploaded_log is None:
        EventData.uploaded_log = EventData.example_log

    start_time = time.perf_counter()
    try:
        if algo == "alpha":
            process_model, start, end = pm4py.discover_petri_net_alpha(EventData.uploaded_log)
        elif algo == "inductive":
            if noise_threshold is None or noise_threshold > 1 or noise_threshold < 0:
                noise_threshold = 0.0
                logging.debug("Noise threshold is not set or not in range [0,1], using default value 0.0")

            process_model, start, end = pm4py.discover_petri_net_inductive(EventData.uploaded_log, noise_threshold)
        elif algo == "heuristic":
            # check values and set to pm4py default values if not in range [0,1]
            if dependency_threshold is None or dependency_threshold > 1 or dependency_threshold < 0:
                dependency_threshold = 0.5
            if and_threshold is None or and_threshold > 1 or and_threshold < 0:
                and_threshold = 0.65
            if loop_two_threshold is None or loop_two_threshold > 1 or loop_two_threshold < 0:
                loop_two_threshold = 0.5
            if min_act_count is None or min_act_count <= 0:
                min_act_count = 1
            if min_dfg_occurrences is None or min_dfg_occurrences <= 0:
                min_dfg_occurrences = 1

            process_model, start, end = pm4py.discover_petri_net_heuristics(EventData.uploaded_log, dependency_threshold, and_threshold, loop_two_threshold, min_act_count, min_dfg_occurrences)
        else:
            logging.error("Algorithm is not chosen")
            return no_update, no_update, no_update, no_update, False, True, no_update
    except Exception as e:
        logging.error(f"Mining went wrong: {e}")
        return no_update, no_update, no_update, no_update, False, True, no_update

    mining_duration = time.perf_counter() - start_time
    mining_duration = "mining duration: "+ str(round(mining_duration,2)) + "s"
    logging.info(f"[{algo}] {mining_duration}")

    try:
        # petri net conversion
        pt = pm4py.convert_to_process_tree(process_model, start, end)
        bpmn = pm4py.convert_to_bpmn(process_model, start, end)
    except Exception as e:
        logging.error(type(e).__name__ + " while converting process model: " + str(e))
        return no_update, no_update, no_update, no_update, True, no_update

    global timestr
    timestr = time.strftime("%Y%m%d-%H%M%S")

    pn_file_name = f"pn_{timestr}.svg"
    bpmn_file_name = f"bpmn_{timestr}.svg"
    pt_file_name = f"pt_{timestr}.svg"

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
        pm4py.save_vis_petri_net(process_model, start, end, pn_file_path)
        pm4py.save_vis_bpmn(bpmn, bpmn_file_path)
        pm4py.save_vis_process_tree(pt, pt_file_path)
    except Exception as e:
        logging.error(type(e).__name__ + " while saving process model: " + str(e))
        return no_update, no_update, no_update, no_update, True, no_update

    # # draw text on pn image
    # img = Image.open(pn_file_path)
    # I1 = ImageDraw.Draw(img)
    # I1.text((0, 0), f"[{algo}]", fill=(255, 0, 0))
    # img.save(pn_file_path)

    return  dash.get_asset_url(pn_file_name),dash.get_asset_url(bpmn_file_name),dash.get_asset_url(pt_file_name),mining_duration, True, False, None