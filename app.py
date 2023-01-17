import base64
import datetime
import io
import time
import pm4py

import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

import pandas as pd

BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css"
table_example = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

data = pd.read_csv('./example_files/running-example.csv', sep=';')
log = pm4py.read_xes('./example_files/running-example.xes')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)


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

app.layout = dbc.Container(
        html.Div(children=[html.Div(
                sidebar
            ),
        dash.page_container,
        ]))

def parse_contents(contents, filename, date):
    """Parse a dash upload component contents."""
    content_type, content_string = contents.split(';')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records')
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


### Upload File Box
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'),
              prevent_initial_call=True)
def update_output(list_of_contents, list_of_names, list_of_dates):
    """Called when file is uploaded."""
    print("Callback 'File upload called'")
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


### Transformation "start mining" Button
@app.callback(
    Output('graphs', 'children'),
    Output('loading-1', 'children'),
    Input('mine-button', 'n_clicks'),
    State('algo-dropdown', 'value'),
    State('graph-dropdown', 'value'),
    prevent_initial_call=True
)
def update_transformation(value, algo, graph):
    """Calles when transformation button is clicked."""
    print("Callback 'start mining' button with value:", value, "and algo:", algo, "and graph:", graph)
    process_model = pm4py.discover_bpmn_inductive(log)
    pm4py.save_vis_bpmn(process_model, "assets/bpmn.png")
    return html.Img(id= "bpmn", src=dash.get_asset_url("bpmn.png"), alt="BPMN Image", style={'width':'100%'}), None


if __name__ == '__main__':
    app.run_server(debug=True)