import dash
from dash import dcc,html

dash.register_page(__name__,path="/data")


layout = html.Div([
    html.H1('Data'),
])