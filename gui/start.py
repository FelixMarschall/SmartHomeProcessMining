"""
Starts Dash based web app to handle interaction
"""

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

class WebAPP:
    '''Handles Dash Application'''
    def __init__(self):
        self.app = Dash(__name__)

        # assume you have a "long-form" data frame
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

            dcc.Graph(
                id='example-graph',
                figure=fig
            )
        ])