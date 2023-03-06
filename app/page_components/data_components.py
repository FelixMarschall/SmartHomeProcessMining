import pandas as pd
from dash import dcc, html, dash_table

def get_data_table(log: pd.DataFrame) -> dash_table.DataTable:
   return dash_table.DataTable(log.to_dict('records'),
        columns= [{"name": i, "id": i} for i in log.columns],
        filter_action='native',
        page_action='none',
        export_format='xlsx',
        export_headers='display',
        style_table={
      'height': '900px',
      #'overflowY': 'auto' # activates scroll within table
      })

def get_logbook_table(log: pd.DataFrame) -> dash_table.DataTable:
   return dash_table.DataTable(log.to_dict('records'),
        columns= [{"name": i, "id": i} for i in log.columns],
        filter_action='native',
        page_action='none',
        export_format='xlsx',
        export_headers='display',
        virtualization=True,
        style_table={
      'height': '1080px',
      #'overflowY': 'auto' # activates scroll within table
      })

def get_upload_button_style() -> dict:
   return {
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }