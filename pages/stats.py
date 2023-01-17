import dash
from dash import dcc,html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import app

dash.register_page(__name__,path="/stats")

data = app.data
fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])


df = px.data.iris()  # iris is a pandas DataFrame
fig2 = px.scatter(df, x="sepal_width", y="sepal_length")

layout = html.Div([
    html.H1('Stats'),
    html.Hr(),
    html.H2('Week View'),
    dcc.Graph(figure=fig),
    html.Hr(),
    html.H2('Month View'),
    dcc.Graph(figure=fig2)])
