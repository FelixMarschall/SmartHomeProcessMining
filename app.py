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

# process mining imports
import pm4py

# local imports
import page_components.data_components as data_components
import page_components.app_components as app_components
import page_components.transformation_components as transformation_components


BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"

# data = pd.read_csv('./example_files/running-example.csv', sep=';')
example_log = pm4py.read_xes('./assets/running-example.xes')
log = None

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

    global log
    if log is None and contents is None:
        logger.debug("No log found, using example log")
        return html.Div(id ="data-table", children=[
        html.Div(id="info-field", children='Example log is displayed below.'),
        data_components.get_data_table(example_log)
    ]),
    elif contents is None:
        return data_components.get_data_table(log)

    CSV_SEPERATOR = ','
    content_type, content_string = contents.split(CSV_SEPERATOR)
    decoded = base64.b64decode(content_string)

    logger.info(f"File uploaded with name: '{list_of_names}' and date: {list_of_dates}")
    
    try:
        if list_of_names.endswith('.csv'):
            UPLOAD_PATH = "assets/temp/uploaded.csv"
            f = open(UPLOAD_PATH, "w")
            f.write(decoded.decode('utf-8'))
            f.close()
            log = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            logger.debug("upload file is csv log")
        elif list_of_names.endswith('.xes'):
            UPLOAD_PATH = "assets/temp/uploaded.xes"
            f = open(UPLOAD_PATH, "w")
            f.write(decoded.decode('utf-8'))
            f.close()
            log = pm4py.read_xes(UPLOAD_PATH)
            logger.debug("upload file is xes log")
    except Exception as e:
        logger.error(type(e).__name__ + " while reading file: " + str(e))
        raise PreventUpdate()

    return data_components.get_data_table(log)

### Transformation "start mining" Button
@app.callback(
    Output('mining-duration', 'children'),
    Output('loading-1', 'children'),
    Output('graphs', 'children'),
    Input('mine-button', 'n_clicks'),
    State('algo-dropdown', 'value'),
    State('graph-dropdown', 'value'),
    prevent_initial_call=False
    #TODO: vill auf false, damit Bilder direkt neu geladen werden.
)
def update_transformation(value, algo, graph):
    """Calles when transformation button is clicked."""
    logger.debug(f"Callback 'start mining' button with value: {value} and algo: {algo} and graph: {graph}")

    global log
    if log is None:
        log = example_log

    start_time = time.perf_counter()

    if algo == "alpha":
        process_model, start, end = pm4py.discover_petri_net_alpha(log)
    elif algo == "inductive":
        process_model, start, end = pm4py.discover_petri_net_inductive(log)
    elif algo == "heuristic":
        process_model, start, end = pm4py.discover_petri_net_heuristics(log)
    else:
        logger.error("Algorithm is not chosen")
        raise PreventUpdate("Algorithm is not chosen")

    mining_duration = time.perf_counter() - start_time
    mining_duration = "mining duration: "+ str(round(mining_duration,2)) + "s"
    logger.info(f"[{algo};{graph}] {mining_duration}")

    try:
        pt = pm4py.convert_to_process_tree(process_model, start, end)
        bpmn = pm4py.convert_to_bpmn(process_model, start, end)
    except Exception as e:
        logger.error(type(e).__name__ + " while converting process model: " + str(e))
        raise PreventUpdate()

    pn_file_name = "pn.png"
    bpmn_file_name = "bpmn.svg"
    pt_file_name = "pt.png"

    try:
        pm4py.save_vis_bpmn(bpmn, f"assets/{bpmn_file_name}")
        pm4py.save_vis_process_tree(pt, f"assets/{pt_file_name}")
        pm4py.save_vis_petri_net(process_model, start, end, f"assets/{pn_file_name}")
    except Exception as e:
        logger.error(type(e).__name__ + " while saving process model: " + str(e))
        raise PreventUpdate()

    # draw text on image
    img = Image.open(f"assets/{pn_file_name}")
    I1 = ImageDraw.Draw(img)
    I1.text((0, 0), f"[{algo};{graph}]", fill=(255, 0, 0))
    img.save(f"assets/{pn_file_name}")

    return  mining_duration, None, transformation_components.get_tranformation_output(dash.get_asset_url(pn_file_name), dash.get_asset_url(bpmn_file_name), dash.get_asset_url(pt_file_name))

if __name__ == '__main__':
    app.run_server(debug=False)