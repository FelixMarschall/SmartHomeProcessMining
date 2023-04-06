import dash
from dash import html

dash.register_page(__name__, path="/", order=0)

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
              html.A('Installation Guide (Home Assistant)',
                     href='https://github.com/FelixMarschall/HA_ProcessMining_Addon/blob/main/process_management/DOCS.md'),
              html.Br(),
              html.A('Installation Guide (Local Machine)',
                     href='https://github.com/FelixMarschall/SmartHomeProcessMining#readme'),
              ]),
    html.Hr(),
    html.H2('How to use this demo?'),
    html.Div('You can import your own logs by clicking on the "Import Log" button.\
             A personal token is neccessary to access the home assistant data, copy the token into the addon configuration and restart the addon.\
             You can export the log as .csv and prepare it for process discovery by adding the following columns: "case_id", "activity", "timestamp" and upload it.'),
    html.Br(),
    html.A("An example for the prepreparation",
           href="https://github.com/FelixMarschall/Logbook-ProcessDiscovery"),
    html.Hr(),
    html.H2('Documentation'),
    html.Div('Shared source code on GitHub: '),
    html.A('Python Application',
           href='https://github.com/FelixMarschall/SmartHomeProcessMining'),
    html.Br(),
    html.A('Home Assistant Addon',
           href='https://github.com/FelixMarschall/HA_ProcessMining_Addon')
])
