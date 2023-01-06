import dash
from dash import dcc,html

dash.register_page(__name__,path="/transformation")


layout = html.Div([
    html.H1('Transformation'),
    ### Transformation
    html.Div(children='Choose your favorite algorithmn and set parameters!'),
    dcc.Dropdown(
    ['Alpha', 'Heuristic', 'Inductive'],
    'Alpha',
    clearable=False,
    id='demo-dropdown',
    style={
        'width': '50%',
        'margin': '10px'
    }),
])
