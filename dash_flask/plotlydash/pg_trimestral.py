import dash_flask.plotlydash.cfg_geral  as cfg
from dash_flask.plotlydash.cfg_geral import *

from dash_flask.plotlydash.cfg_trimestral import *

def init_trimestral(server):
    app = Dash(server=server, routes_pathname_prefix="/trimestral/", external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(children=[

        dbc.Row([
            html.Div([
                html.Img(src="../static/assets/logo-stefanini-preto.svg", style={'width': '150px', 'height': '50px'}),

                    html.Div(
                        dcc.RadioItems(['Trimestral', 'Mensal'], 'Mensal', id='radio', style={'width': '100px'}),
                        style={'width': 'auto', 'margin-left': '10px'}
                    ),

                    html.Div(
                        dcc.Dropdown(lista_ano(), str(data.year), placeholder='ANO', id='drop_ano'),
                        style={'min-width': '120px', 'margin-left': '10px'}
                    ),

                    html.Div(
                        dcc.Dropdown(lista_mes(), str(data.month), placeholder='PERIODO', id='drop_mes'), id='COMBOMES',
                        style={'width': '120px', 'margin-left': '10px'}
                    )
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
        html.Div(id='layout', style={'background-color': '#1c1d21', 'margin-top': '60px'}),
        html.Div(id='teste')
    ])

    @callback(
        Output('COMBOMES', component_property='children'),
        Input(component_id='radio', component_property='value'), prevent_initial_call=True
    )
    def change_dropdown(radio):
        if radio == 'Trimestral':
            return dcc.Dropdown(lista_trimestral(), placeholder='PERIODO', id='drop_mes', style={'width': '100%'})
        else:
            return dcc.Dropdown(lista_mes(), placeholder='PERIODO', id='drop_mes', style={'width': '100%'})


    @callback(
        Output('layout', component_property='children'),
        [Input('drop_mes', component_property='value'),
         Input('drop_ano', component_property='value')]
    )
    def build_layout(drop_mes, drop_ano):
        if drop_mes is None or drop_ano is None:
            html = ""
            return html

        cfg.ano = drop_ano

        if len(str(drop_mes)) > 2:
            cfg.mes_inicio = str(drop_mes[0]) + str(drop_mes[1])
            cfg.mes_fim = str(drop_mes[-2]) + str(drop_mes[-1])
            html = l_chamados()
            return html
        else:
            cfg.mes_inicio = drop_mes
            cfg.mes_fim = drop_mes
            html = l_chamados()
            return html

    return app.server