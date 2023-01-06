import dash
from dash import dcc,html, dash_table
import pandas as pd

dash.register_page(__name__,path="/data")

#df = pd.read_csv('./example_files/running-example.csv', sep=';')


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
    html.Div(children='Your event log is displayed below.'),
    html.Div(id="output-data-upload", children=[]),
    dash_table.DataTable(SmartHomeLog.get_data().to_dict('records'),
        columns= [{"name": i, "id": i} for i in SmartHomeLog.get_data().columns],
        filter_action='native',
        page_action='none',
        style_table={'height': '900px', 'overflowY': 'auto'}),
])