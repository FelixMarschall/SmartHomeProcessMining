import dash
from dash import dcc,html

import pandas as pd

dash.register_page(__name__,path="/transformation")

data = pd.read_csv('./example_files/running-example.csv', sep=';')

layout = html.Div([
    html.H1('Transformation'),
    ### Transformation
    html.Div(children='Choose your favorite algorithmn and set parameters!'),
    dcc.Dropdown(
    ['Alpha', 'Heuristic', 'Inductive', 'Fuzzy'],
    'Alpha',
    clearable=False,
    id='algo-dropdown',
    style={
        'width': '50%',
        'margin': '10px'
    }),
    dcc.Dropdown(
    ['Petri Net', 'Process Tree', 'BPMN'],
    'Petri Net',
    clearable=False,
    id='graph-dropdown',
    style={
        'width': '50%',
        'margin': '10px'
    }),
    html.H2('Parameters'),
    html.Button('Start mining', id='mine-button'),
    html.Hr(),
    html.H2('Petri Net'),
    html.Div(id='container-button-basic',
             children=[html.Img(id= "bpmn", src=dash.get_asset_url("bpmn.png"), alt="BPMN Image", style={'width':'100%'})]),
    html.Hr(),
    html.H2('BPMN Graph'),
    html.Img(id= "petrinet", src=dash.get_asset_url("net.svg"), alt="Petri Net Image", style={'width':'100%'}),
    html.Hr(),
# html.Img(id= "bpmn", src=dash.get_asset_url("bpmn.png"), alt="BPMN Image", style={'width':'100%'}),
])


