import dash
from dash import dcc,html
import pandas as pd

import page_components.components as components
import page_components.transformation_components as transformation_components

dash.register_page(__name__,path="/transformation", order=4)

layout = html.Div([
    html.H1('Transformation'),
    html.Hr(),
    ### Transformation
    html.Div(children='Choose your favorite algorithmn and set parameters!'),
    dcc.Dropdown(
    ['alpha', 'heuristic', 'inductive'],
    value='alpha',
    clearable=False,
    id='algo-dropdown',
    style={
        'width': '50%',
        'margin': '10px'
    }),
    # dcc.Dropdown(
    # ['Petri Net', 'Process Tree', 'BPMN'],
    # 'Petri Net',
    # clearable=False,
    # id='graph-dropdown',
    # style={
    #     'width': '50%',
    #     'margin': '10px'
    # }),
    dcc.Loading(
            id="loading-1",
            type="circle",
            children=html.Div(id="loading-output-1")
        ),
    html.H2('Parameters'),
    html.Div(id='alpha-parameters', children="No parameters available for Alpha Miner", hidden=True),
    html.Div(id='inductive-parameters', children=
        [
            html.Label('Noise Threshold', style=transformation_components.get_parameter_input_style()),
            dcc.Input(id='noise_threshold', type='number', min=0.0, max=1.0, step=0.1, value=0.0),
        ],
        hidden=True
    ),
    html.Div(id='heuristic-parameters', children=
        [
            html.Label('Dependency Threshold', style=transformation_components.get_parameter_input_style()),
            dcc.Input(id='dependency_threshold', type='number', min=0.0, max=1.0, step=0.1, value=0.5), #float

            html.Label('AND Threshold', style=transformation_components.get_parameter_input_style()), 
            dcc.Input(id='and_threshold', type='number', min=0.0, max=1.0, step=0.1, value=0.5), #float
            
            html.Label('Loop Two Threshold', style=transformation_components.get_parameter_input_style()),
            dcc.Input(id='loop_two_threshold', type='number', min=0.0, max=1.0, step=0.1, value=0.5), #float

            html.Label('min act count', style=transformation_components.get_parameter_input_style()),
            dcc.Input(id='min_act_count', type='number', min=1, step=1, value=1, pattern=u"^[0-9]\d*$"), # int

            html.Label('min dfg occurrences', style=transformation_components.get_parameter_input_style()),
            dcc.Input(id='min_dfg_occurrences', type='number', min=1, step=1, value=1, pattern=u"^[0-9]\d*$"), # int
        ],
        hidden=True
    ),
    html.Hr(),
    html.Button('Start mining', id='mine-button', 
                    style=components.get_button_style()),
    html.Div(id='mining-duration'),
    html.Div(id='graphs',
             children=[
                html.Hr(),
                html.H2('Petri Net'),
                html.Img(id= "petrinet", src=dash.get_asset_url("pn.png"), alt="Petri Net Image", style={'width':'100%'}),
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


