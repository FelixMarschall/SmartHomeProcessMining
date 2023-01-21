import pandas as pd
from dash import dcc, html, dash_table


def get_data_table(log: pd.DataFrame) -> dash_table.DataTable:
   return dash_table.DataTable(log.to_dict('records'),
        columns= [{"name": i, "id": i} for i in log.columns],
        filter_action='native',
        page_action='none',
        style_table={'height': '900px', 'overflowY': 'auto'})