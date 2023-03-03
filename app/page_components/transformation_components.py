import pandas as pd
from dash import dcc, html, dash_table

def get_tranformation_output(pn, bpmn, pt) -> html.Div:
    return [
        html.Hr(),
        html.H2('Updated Petri Net'),
        html.Img(id= "petrinet", src=pn, alt="Petri Net Image Default", style={'width':'100%'}),
        html.Hr(),
        html.H2('BPMN Graph'),
        html.Img(id= "bpmn", src=bpmn, alt="BPMN Image Default", style={'width':'100%'}),
        html.Hr(),
        html.H2('Process Tree'),
        html.Img(id= "processtree", src=pt, alt="Process Tree Default", style={'width':'100%'}),
        html.Hr()
        ]

def get_parameter_input_style():
    return {
        'margin-right': '20px',
        'margin-left': '30px'
    }