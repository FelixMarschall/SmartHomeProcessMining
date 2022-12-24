"""Application starts here"""

from gui.start import WebAPP

if __name__ == '__main__':
    dash = WebAPP()
    dash.app.run_server(debug=True)