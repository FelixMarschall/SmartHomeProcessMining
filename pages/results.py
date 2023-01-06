import dash
from dash import dcc,html

dash.register_page(__name__,path="/results")


layout = html.Div([
    html.H1('Results'),
])