import dash
from dash import dcc,html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

import pm4py

dash.register_page(__name__,path="/stats", order=3)

fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

log = pm4py.read_xes('./app/assets/running-example.xes')

count_activities = px.bar(log["concept:name"].value_counts())


cluster_by_day = log[["time:timestamp", "concept:name"]].groupby(pd.Grouper(key="time:timestamp", freq="D")).count()

count_events = px.bar(log["concept:name"].value_counts())


df = px.data.iris()  # iris is a pandas DataFrame
fig2 = px.scatter(df, x="sepal_width", y="sepal_length")

layout = html.Div(id= "stats", children = [
    html.H1('Stats'),
    html.P('Depicts statistics of the uploaded event log.'),
    html.Hr(),
    html.H2('Activities'),
    dcc.Graph(figure=count_activities),
    html.H2('Day View'),
    html.P('Number of events per day'),
    dcc.Graph(figure=px.bar(cluster_by_day)),
    html.Hr(),
    html.H2('Week View'),
    dcc.Graph(figure=fig),
    html.Hr(),
    html.H2('Month View'),
    dcc.Graph(figure=fig2)])

