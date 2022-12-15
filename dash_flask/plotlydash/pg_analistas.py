import dash_flask.plotlydash.cfg_geral  as cfg
from dash_flask.plotlydash.cfg_geral import *

import dash_flask.plotlydash.cfg_analistas  as cfg_analistas
from dash_flask.plotlydash.cfg_analistas import *

def init_analistas(server):
    app = Dash(server=server, routes_pathname_prefix="/analistas/", external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(children=[

        dbc.Row([
            html.Div([
                html.Img(src="../static/assets/logo-stefanini-preto.svg", style={'width': '150px', 'height': '50px'}),

                html.Div([
                    dcc.Dropdown(lista_ano(), str(data.year), placeholder='ANO', id='DPANO')
                ], style={'min-width': '120px', 'margin-left': '20px'}),

                html.Div([
                    dcc.Dropdown(lista_mes(), str(data.month), placeholder='MES', id='DPMES')
                ], style={'min-width': '120px', 'margin-left': '20px'}),

                dcc.RadioItems(['Todos', 'Comparar'], 'Todos', id='radio', style={'width': '100px', 'margin-left': '20px'}),

                html.Div([
                    dcc.Dropdown(analista(), multi=True, placeholder='ANALISTAS', id="combo")
                ], style={'min-width': '170px', 'margin-left': '20px', 'display': 'none'}, id="comboanalista")
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
        html.Div(id='layout', style={'background-color': '#1c1d21', 'margin-top': '70px'}),
    ])

    @app.callback(
        [Output('comboanalista', component_property='style'),
         Output('layout', component_property='children')],
        [Input(component_id='DPANO', component_property='value'),
         Input(component_id='DPMES', component_property='value'),
         Input(component_id='radio', component_property='value'),
         Input(component_id='combo', component_property='value')]
    )
    def change(DPANO, DPMES, radio, combo):

        if DPANO is None or DPMES is None:
            if radio == 'Todos':
                return {'display': 'none'}, html.Div()
            else:
                return {'display': 'block', 'min-width': '170px', 'margin-left': '20px'}, html.Div()

        cfg.ano = DPANO
        cfg.mes_inicio = DPMES
        cfg.mes_fim = DPMES

        if radio == 'Todos':
            cfg_analistas.analistas = analista()
            page = l_analistas()
            return {'display': 'none'}, page
        else:
            if combo == None:
                return {'display': 'block', 'min-width': '170px', 'margin-left': '20px'}, html.Div()
            else:
                cfg_analistas.analistas = combo
                page = l_analistas()
                return {'display': 'block', 'min-width': '170px', 'margin-left': '20px'}, page

    return app.server
