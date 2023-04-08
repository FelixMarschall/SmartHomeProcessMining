# Smart Home Process Mining
Uses Process Mining to extract Smart Home information from an Event Log. 


## Local installation
### Requirements
- Python3 with pip
- Graphviz installation.

### Installation

1. `git clone https://github.com/FelixMarschall/SmartHomeProcessMining`
2. `cd SmartHomeProcessMining/`
3. `pip install -r requirements.txt`
4. `python3 app/app.py`

## Access Home-Assistant Data remotely

1. Create a new personal long-term token in home-assistant
2. open the `SmartHomeProcessMining` folder
3. open `config.yaml`
4. change `token`

Caution: updating this app can flush token!

## Home-Assistant add-on installation
https://github.com/FelixMarschall/HA_ProcessMining_Addon
