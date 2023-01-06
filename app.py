import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd

df = pd.read_csv('./example_files/running-example.csv', sep=';')

BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
table_example = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(children=[
    html.H1(children='Smart Home Process Mining'),

    html.Div(children='''
        A web application for Process Mining with your Smart home data.
    '''),
    ### Input
    html.H2(children='Input'),
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
dash_table.DataTable(df.to_dict('records'),
    columns= [{"name": i, "id": i} for i in df.columns],
    filter_action='native',
    page_action='none',
    style_table={'height': '300px', 'overflowY': 'auto'}),

### Preprocessing
html.H2(children='Preprocessing'),
### Transformation
html.H2(children='Transformation'),
html.Div(children='Choose your favorite algorithmn and set parameters!'),
dcc.Dropdown(
['Alpha', 'Heuristic', 'Inductive'],
'Alpha',
clearable=False,
id='demo-dropdown',
style={
    'width': '50%',
    'margin': '10px'
},
),
### Output
html.Div(id='dd-output-container'),
html.H2(children='Output')
#, 
# html.Div(id='output-data-upload'),
#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
])

def parse_contents(contents, filename, date):
    """Parse a dash upload component contents."""
    content_type, content_string = contents.split(';')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records')
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])



@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    """Called when file is uploaded."""
    print("Callback File upload called")



    # if list_of_contents is not None:
    #     children = [
    #         parse_contents(c, n, d) for c, n, d in
    #         zip(list_of_contents, list_of_names, list_of_dates)]
    #     return children

if __name__ == '__main__':
    app.run_server(debug=True)