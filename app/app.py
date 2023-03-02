import base64
import io
import time
import logging
from PIL import Image
from PIL import ImageDraw

# imports for web app
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd

# own modules
from homeassistant import Api

# process mining imports
import pm4py

# local imports
import page_components.data_components as data_components
import page_components.app_components as app_components
import page_components.transformation_components as transformation_components

import os

print("\n",os.environ,"\n")

BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"

PATH_ASSETS = "./app/assets/"

# data = pd.read_csv('./example_files/running-example.csv', sep=';')
example_log = pm4py.read_xes(PATH_ASSETS + 'running-example.xes')

uploaded_log = None

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

# set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app.layout = app_components.get_layout()

### Upload File Box
@app.callback(Output('data-table', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              prevent_initial_call=False)
def update_output(contents, list_of_names, list_of_dates):
    """Called when file is uploaded."""
    logger.debug("Callback 'File upload called'")

    global uploaded_log
    if uploaded_log is None and contents is None:
        logger.debug("No log found, using example log")
        return html.Div(id ="data-table", children=[
        html.Div(id="info-field", children='Example log is displayed below.'),
        data_components.get_data_table(example_log)
    ]),
    elif contents is None:
        return data_components.get_data_table(uploaded_log)

    CSV_SEPERATOR = ','
    content_type, content_string = contents.split(CSV_SEPERATOR)
    decoded = base64.b64decode(content_string)

    logger.info(f"File uploaded with name: '{list_of_names}' and date: {list_of_dates}")
    
    try:
        if list_of_names.endswith('.csv'):
            UPLOAD_PATH = PATH_ASSETS + "/temp/uploaded.csv"
            f = open(UPLOAD_PATH, "w")
            f.write(decoded.decode('utf-8'))
            f.close()
            uploaded_log = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            logger.debug("upload file is csv log")
        elif list_of_names.endswith('.xes'):
            UPLOAD_PATH = PATH_ASSETS + "/temp/uploaded.xes"
            f = open(UPLOAD_PATH, "w")
            f.write(decoded.decode('utf-8'))
            f.close()
            uploaded_log = pm4py.read_xes(UPLOAD_PATH)
            logger.debug("upload file is xes log")
    except Exception as e:
        logger.error(type(e).__name__ + " while reading file: " + str(e))
        raise PreventUpdate()

    # update stats page
    
    return data_components.get_data_table(uploaded_log)

### Transformation "start mining" Button
@app.callback(
    Output('mining-duration', 'children'),
    Output('loading-1', 'children'),
    Output('graphs', 'children'),
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
    #TODO: vill auf false, damit Bilder direkt neu geladen werden.
)
def update_transformation(value, algo, noise_threshold, dependency_threshold, and_threshold, loop_two_threshold, min_act_count, min_dfg_occurrences):
    """Calles when transformation button is clicked."""
    logger.debug(f"Callback 'start mining' button with value: {value} and algo: {algo}")

    global uploaded_log
    if uploaded_log is None:
        uploaded_log = example_log

    start_time = time.perf_counter()

    if algo == "alpha":
        process_model, start, end = pm4py.discover_petri_net_alpha(uploaded_log)
    elif algo == "inductive":
        if noise_threshold is None or noise_threshold > 1 or noise_threshold < 0:
            noise_threshold = 0.0
            logger.debug("Noise threshold is not set or not in range [0,1], using default value 0.0")

        process_model, start, end = pm4py.discover_petri_net_inductive(uploaded_log, noise_threshold)
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

        process_model, start, end = pm4py.discover_petri_net_heuristics(uploaded_log, dependency_threshold, and_threshold, loop_two_threshold, min_act_count, min_dfg_occurrences)
    else:
        logger.error("Algorithm is not chosen")
        raise PreventUpdate("Algorithm is not chosen")

    mining_duration = time.perf_counter() - start_time
    mining_duration = "mining duration: "+ str(round(mining_duration,2)) + "s"
    logger.info(f"[{algo}] {mining_duration}")

    try:
        pt = pm4py.convert_to_process_tree(process_model, start, end)
        bpmn = pm4py.convert_to_bpmn(process_model, start, end)
    except Exception as e:
        logger.error(type(e).__name__ + " while converting process model: " + str(e))
        raise PreventUpdate()

    pn_file_name = "pn.png"
    bpmn_file_name = "bpmn.svg"
    pt_file_name = "pt.png"

    pn_file_path = PATH_ASSETS + pn_file_name
    bpmn_file_path = PATH_ASSETS + bpmn_file_name
    pt_file_path = PATH_ASSETS + pt_file_name

    try:
        pm4py.save_vis_bpmn(bpmn, bpmn_file_path)
        pm4py.save_vis_process_tree(pt, pt_file_path)
        pm4py.save_vis_petri_net(process_model, start, end, pn_file_path)
    except Exception as e:
        logger.error(type(e).__name__ + " while saving process model: " + str(e))
        raise PreventUpdate("Error while saving process model")

    # draw text on pn image
    img = Image.open(pn_file_path)
    I1 = ImageDraw.Draw(img)
    I1.text((0, 0), f"[{algo}]", fill=(255, 0, 0))
    img.save(pn_file_path)

    return  mining_duration, None, transformation_components.get_tranformation_output(dash.get_asset_url(pn_file_name), dash.get_asset_url(bpmn_file_name), dash.get_asset_url(pt_file_name))


### Hide/Show Parameters for Transformation Algorithms
@app.callback(
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

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")