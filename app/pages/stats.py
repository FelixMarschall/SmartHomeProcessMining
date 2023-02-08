import dash
from dash import dcc,html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

import pm4py

dash.register_page(__name__,path="/stats")

fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

log = pm4py.read_xes('./assets/running-example.xes')
count_activities = px.bar(log["concept:name"].value_counts())

df = px.data.iris()  # iris is a pandas DataFrame
fig2 = px.scatter(df, x="sepal_width", y="sepal_length")

layout = html.Div(id= "stats", children = [
    html.H1('Stats'),
    html.Hr(),
    dcc.Graph(figure=count_activities),
    html.H2('Day View'),
    dcc.Graph(figure=fig),
    html.Hr(),
    html.H2('Week View'),
    dcc.Graph(figure=fig),
    html.Hr(),
    html.H2('Month View'),
    dcc.Graph(figure=fig2)])
