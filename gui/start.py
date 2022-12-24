"""
Starts Dash based web app to handle interaction
"""

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

class WebAPP:
    '''Handles Dash Application'''
    def __init__(self):
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.app = Dash(__name__, external_stylesheets=external_stylesheets)

        # see https://plotly.com/python/px-arguments/ for more options
        df = pd.DataFrame({
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
        })

        fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

        self.app.layout = html.Div(children=[
            html.H1(children='Smart Home Process Mining'),

            html.Div(children='''
                A web application for Process Mining with your Smart home data.
            '''),
            html.H2(children='Input'),
            dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Event Log File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Forbid multiple files to be uploaded
        multiple=False
    ),
    html.H2(children='Preprocessing'),
    html.H2(children='Transformation'),
    html.Div(children='Choose your favorite algorithmn and set parameters!'),
    html.H2(children='Output'),
    html.Div(id='output-data-upload'),
            dcc.Graph(
                id='example-graph',
                figure=fig
            )
        ])