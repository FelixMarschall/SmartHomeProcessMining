import os
import dash
from dash import dcc, html, Input, Output, callback
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from event_data import EventData

dash.register_page(__name__, path="/stats", order=3)


layout = html.Div(id="stats", children=[
    html.H1('Stats'),
    html.P('Depicts statistics of the uploaded event log.'),
    dcc.Loading(
        id="loading-stats",
        type="circle",
        children=html.Div(id="loading-output-1")
    ),
    html.Hr(),
    html.H2('Activities'),
    html.P('Absolute number of events per activity'),
    dcc.Graph(id="activities"),
    html.H2('Day View'),
    html.P('Number of events per day'),
    dcc.Graph(id="day"),
    html.Hr(),
    html.H2('Week View'),
    dcc.Graph(id="week"),
    html.Hr(),
    html.H2('Month View'),
    dcc.Graph(id="month"),
    html.Div(id="dummy")
]
)


@callback(
    Output("activities", "figure"),
    Output("day", "figure"),
    Output("week", "figure"),
    Output("month", "figure"),
    Output("loading-stats", "children"),
    Input("dummy", "children")
)
def update_stats(dummy):
    if EventData.uploaded_log is not None:
        EventData.uploaded_log["time:timestamp"] = pd.to_datetime(
            EventData.uploaded_log['time:timestamp'])
        log = EventData.uploaded_log
    else:
        log = EventData.example_log

    count_activities = px.bar(log["concept:name"].value_counts())

    cluster_by_day = log[["time:timestamp", "concept:name"]].groupby(
        pd.Grouper(key="time:timestamp", freq="D")).count()

    count_events = px.bar(log["concept:name"].value_counts())

    df = px.data.iris()  # iris is a pandas DataFrame
    fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
    fig2 = px.scatter(df, x="sepal_width", y="sepal_length")

    return count_activities, px.bar(cluster_by_day), fig, fig2, None
