import pandas as pd
from dash import dcc, html, dash_table

def get_tranformation_output(pn, bpmn, pt) -> html.Div:
    return [
        html.Hr(),
        html.H2('Petri Net'),
        html.Img(id= "petrinet", src=pn, alt="Petri Net Image", style={'width':'100%'}),
        html.Hr(),
        html.H2('BPMN Graph'),
        html.Img(id= "bpmn", src=bpmn, alt="BPMN Image", style={'width':'100%'}),
        html.Hr(),
        html.H2('Process Tree'),
        html.Img(id= "processtree", src=pt, alt="Process Tree", style={'width':'100%'}),
        html.Hr()
        ]