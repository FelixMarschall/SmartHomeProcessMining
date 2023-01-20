import dash
from dash import dcc,html, dash_table
import pandas as pd
import pm4py

dash.register_page(__name__,path="/data")

#df = pm4py.read_xes('./assets/running-example.xes')


layout = html.Div([
    html.H1('Data'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Event Log File')
        ]),
        # Forbid multiple files to be uploaded
        multiple=False,
        style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                }),
    ### Table
    html.Div(id ="data-table", children=[
        html.Div(id="info-field", children='Loading...'),
    ]),
])