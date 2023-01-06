import dash
from dash import dcc, html

dash.register_page(__name__,path="/")


layout = html.Div([
    html.H1('Process Mining with Smart Home Data'),
    html.Div('Import your first log and start with process mining!'),
])
