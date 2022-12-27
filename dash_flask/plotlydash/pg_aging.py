import dash_flask.plotlydash.cfg_geral as cfg
from dash_flask.plotlydash.cfg_geral import *

import dash_flask.plotlydash.cfg_aging as cfg_aging
from dash_flask.plotlydash.cfg_aging import *

def init_aging(server):
    app = Dash(server=server, routes_pathname_prefix="/aging/", external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(children=[

        dbc.Row([
            html.Div([
                html.Img(src="../static/assets/logo-stefanini-preto.svg", style={'width': '150px', 'height': '50px'}),
            ], style={
                'display': 'flex',
                'background-color': '#99CCFF',
                'align-items': 'center',
                'justify-content': 'flex-start',
                'position': 'fixed',
                'z-index': '1',
                'padding-top': '10px',
                'padding-bottom': '10px',
                'height': 'auto',
                'width': '100vw'
            })

        ], className="g-0"),
        html.Div([
            dt_table()
        ], id='layout', style={'background-color': '#1c1d21', 'margin-top': '60px'}),
    ])

    return app.server