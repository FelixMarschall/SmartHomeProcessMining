import dash
from dash import dcc,html, dash_table
import dash_bootstrap_components as dbc


def get_layout():
    return dbc.Container(
        html.Div(children=[html.Div(
                get_sidebar(),
            ),
        dash.page_container,
        ]))

def get_sidebar():
    sidebar = dbc.Nav(
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