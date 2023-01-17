import dash
from dash import dcc,html
import pandas as pd

dash.register_page(__name__,path="/transformation")

layout = html.Div([
    html.H1('Transformation'),
    ### Transformation
    html.Div(children='Choose your favorite algorithmn and set parameters!'),
    dcc.Dropdown(
    ['alpha', 'heuristic', 'inductive', 'fuzzy'],
    'alpha',
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
    dcc.Loading(
            id="loading-1",
            type="circle",
            children=html.Div(id="loading-output-1")
        ),
    html.H2('Parameters'),
    html.Button('Start mining', id='mine-button'),
    html.Div(id='mining-duration'),
    html.Hr(),
    html.H2('Petri Net'),
    html.Div(id='graphs',
             children=[
                html.Img(id= "petrinet", src=dash.get_asset_url("pn.svg"), alt="Petri Net Image", style={'width':'100%'}),
                html.Hr(),
                html.H2('BPMN Graph'),
                html.Img(id= "bpmn", src=dash.get_asset_url("bpmn.svg"), alt="BPMN Image", style={'width':'100%'}),
                html.Hr(),
                html.H2('Process Tree'),
                html.Img(id= "processtree", src=dash.get_asset_url("pt.png"), alt="Process Tree", style={'width':'100%'}),
                html.Hr(),
    ]
    ),
])


