import dash
from dash import dcc,html, dash_table
import pandas as pd

import page_components.data_components as data_components

dash.register_page(__name__,path="/data")

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
        style=data_components.get_upload_button_style()),
    ### Table
    html.Div(id ="data-table", children=[
        html.Div(id="info-field", children='Loading...'),
    ]),
])