import dash
from dash import dcc, html

dash.register_page(__name__,path="/",order=0)

layout = html.Div([
    html.H1('Process Mining with Smart Home Data'),
    html.Div('Import your first log and start with process mining!'),
    html.Div(),
    html.Hr(),
    html.H2('What can I do here?'),
    html.Div(['This is a demo of the process mining capabilities of the Smart Home Data Analytics Platform. You can import your own logs and start with process mining.', 
             html.Br(),
             'You can also access your Home Assistant Logbook when you run it as addon or your homeassistant instance is in the same network and this application got access with a personal token.',
             html.Br(),
            html.A('Installation Guide', href=' https://github.com/FelixMarschall/HA_ProcessMining_Addon/blob/main/process_management/DOCS.md'),
]),
    html.Hr(),
    html.H2('How to use this demo?'),
    html.Div('You can import your own logs by clicking on the "Import Log" button. You can also use the example logs provided in the example files folder. You can also use the example logs provided in the example files folder.'),
    html.Hr(),
    html.H2('Documentation'),
    html.Div('Shared source code on GitHub: '),
    html.A('The Python Application', href='https://github.com/FelixMarschall/SmartHomeProcessMining'),
    html.Br(),
    html.A('The Addon Wrapper', href='https://github.com/FelixMarschall/HA_ProcessMining_Addon')
])
