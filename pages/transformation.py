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
    id='demo-dropdown',
    style={
        'width': '50%',
        'margin': '10px'
    }),
    dcc.Dropdown(
    ['Petri Net', 'Process Tree', 'BPMN'],
    'Petri Net',
    clearable=False,
    id='demo-dropdown',
    style={
        'width': '50%',
        'margin': '10px'
    }),
    html.H2('Parameters'),
    html.Button('Start mining', id='mine-button'),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit'), 
    
])
