import base64
import datetime
import io
import time
import pm4py
import logging

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import pandas as pd

BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"

# data = pd.read_csv('./example_files/running-example.csv', sep=';')
example_log = pm4py.read_xes('./assets/running-example.xes')
log = None
print("New init")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

# set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ], 
    pills=True,
    fill=True)

app.layout = dbc.Container(
        html.Div(children=[html.Div(
                sidebar
            ),
        dash.page_container,
        ]))

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
        dash_table.DataTable(example_log.to_dict('records'),
        columns= [{"name": i, "id": i} for i in example_log.columns],
        filter_action='native',
        page_action='none',
        style_table={'height': '900px', 'overflowY': 'auto'})
    ]),
    elif contents is None:
        return dash_table.DataTable(log.to_dict('records'),
        columns= [{"name": i, "id": i} for i in log.columns],
        filter_action='native',
        page_action='none',
        style_table={'height': '900px', 'overflowY': 'auto'})

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

    return dash_table.DataTable(log.to_dict('records'),
        columns= [{"name": i, "id": i} for i in log.columns],
        filter_action='native',
        page_action='none',
        style_table={'height': '900px', 'overflowY': 'auto'})

    #return log.to_json(date_format='iso', orient='split')

### Transformation "start mining" Button
@app.callback(
    Output('bpmn', 'src'),
    Output('petrinet', 'src'),
    Output('processtree', 'src'),
    Output('mining-duration', 'children'),
    Output('loading-1', 'children'),
    Input('mine-button', 'n_clicks'),
    State('algo-dropdown', 'value'),
    State('graph-dropdown', 'value'),
    prevent_initial_call=True
)
def update_transformation(value, algo, graph):
    """Calles when transformation button is clicked."""
    logger.debug(f"Callback 'start mining' button with value: {value} and algo: {algo} and graph: {graph}")

    # if log == None:
        # log = example_log

    start_time = time.perf_counter()

    if algo == "alpha":
        process_model, start, end = pm4py.discover_petri_net_alpha(log)
    elif algo == "inductive":
        process_model, start, end = pm4py.discover_petri_net_inductive(log)
    elif algo == "heuristic":
        process_model, start, end = pm4py.discover_petri_net_heuristics(log)
    else:
        logger.error("Algorithm not supported")
        raise ValueError("Algorithm not supported")

    mining_duration = time.perf_counter() - start_time
    mining_duration = "mining duration: "+ str(round(mining_duration,2)) + "s"
    logger.info("Duration of mining: " + mining_duration)

    pt = pm4py.convert_to_process_tree(process_model, start, end)
    bpmn = pm4py.convert_to_bpmn(process_model, start, end)

    pm4py.save_vis_bpmn(bpmn, "assets/bpmn.svg")
    pm4py.save_vis_process_tree(pt, "assets/pt.png")
    pm4py.save_vis_petri_net(process_model, start, end, "assets/pn.svg")

    return dash.get_asset_url("bpmn.svg"), dash.get_asset_url("pn.svg"), dash.get_asset_url("pt.png"),mining_duration, None

if __name__ == '__main__':
    app.run_server(debug=True)