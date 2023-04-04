import dash
import logging
import io
import pm4py
from dash import dcc, html, Input, Output, callback, State
from dash.exceptions import PreventUpdate
import pandas as pd
import base64

import page_components.data_components as data_components
from event_data import EventData

import pyarrow.feather as feather

dash.register_page(__name__,path="/data", order=2)

PATH_ASSETS = "./app/assets/"
PATH_IMAGES = PATH_ASSETS + "images/"

layout = html.Div([
    html.H1('Data'),
    html.Hr(),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Event Log File')
        ]),
        # Forbid multiple files to be uploaded
        multiple=False,
        style=data_components.get_upload_button_style()),
    html.Hr(),
    ### Table
    html.Div(id ="data-table", children=[
        html.Div(id="info-field", children='Loading...'),
    ]),
])

### Upload File Box
@callback(Output('data-table', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              prevent_initial_call=False)
def update_output(contents, list_of_names, list_of_dates):
    """Called when file is uploaded."""

    if EventData.uploaded_log is None and contents is None:
        return html.Div(id ="data-table", children=[
        html.Div(id="info-field", children='Example log is displayed below.'),
        data_components.get_data_table(EventData.example_log)
    ]),
    elif contents is None:
        return data_components.get_data_table(EventData.uploaded_log)

    CSV_SEPERATOR = ','
    content_type, content_string = contents.split(CSV_SEPERATOR)
    decoded = base64.b64decode(content_string)

    logging.info(f"File uploaded with name: '{list_of_names}' and date: {list_of_dates}")
    
    try:
        if list_of_names.endswith('.csv'):
            UPLOAD_PATH = PATH_ASSETS + "/temp/uploaded.csv"
            f = open(UPLOAD_PATH, "w")
            f.write(decoded.decode('utf-8'))
            f.close()
            EventData.uploaded_log = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

            feather.write_feather(EventData.uploaded_log, 'app/assets/temp/uploaded.feather')

            logging.debug("upload file is csv log")
        elif list_of_names.endswith('.xes'):
            UPLOAD_PATH = PATH_ASSETS + "/temp/uploaded.xes"
            f = open(UPLOAD_PATH, "w")
            f.write(decoded.decode('utf-8'))
            f.close()
            EventData.uploaded_log = pm4py.read_xes(UPLOAD_PATH)

            feather.write_feather(EventData.uploaded_log, 'app/assets/temp/uploaded.feather')
            
            logging.debug("upload file is xes log")
    except Exception as e:
        logging.error(type(e).__name__ + " while reading file: " + str(e))
        raise PreventUpdate()

    # update stats page
    return data_components.get_data_table(EventData.uploaded_log)