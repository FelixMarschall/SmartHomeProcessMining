import dash
from dash import dcc,html
import dash_bootstrap_components as dbc


def get_layout() -> dbc.Container:
    sidebar = get_sidebar()
    return dbc.Container(
        html.Div(children=[html.Div(
                sidebar,
            ),
        dcc.Store(id='image_file_name', storage_type='session'),
        dcc.Store(id='transformation_parameters', storage_type='session'),
        dash.page_container,
        ]))

def get_sidebar() -> dbc.Nav:
    return dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ], 
    pills=True,
    fill=True)