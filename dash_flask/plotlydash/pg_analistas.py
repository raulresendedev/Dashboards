from dash_flask.plotlydash import cfg_analistas

from dash_flask.plotlydash.cfg_analistas import *


def init_analistas(server):
    app = Dash(server=server, routes_pathname_prefix="/analistas/", external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(children=[

        dbc.Row([
            html.Div([
                html.Img(src="../static/assets/logo-stefanini-preto.svg", style={'width': '150px', 'height': '50px'}),

                html.Div([
                    dcc.Dropdown(lista_ano(), placeholder='ANO', id='DPANO')
                ], style={'min-width': '70px', 'margin-left': '20px'}),

                html.Div([
                    dcc.Dropdown(lista_mes(), placeholder='MES', id='DPMES')
                ], style={'min-width': '70px', 'margin-left': '20px'}),

                dcc.RadioItems(['Todos', 'Comparar'], id='radio', style={'width': '100px', 'margin-left': '20px'}),

                html.Div([
                    dcc.Dropdown(analista(), multi=True, placeholder='ANALISTAS', id="combo")
                ], style={'min-width': '170px', 'margin-left': '20px'}, id="comboanalista")
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
        [Output('comboanalista', component_property='style'), Output('layout', component_property='children')],
        [Input(component_id='DPANO', component_property='value'),
         Input(component_id='DPMES', component_property='value'),
         Input(component_id='radio', component_property='value'),
         Input(component_id='combo', component_property='value')], prevent_initial_call=True
    )
    def change(DPANO, DPMES, radio, combo):

        if DPANO == None:
            data = date.today()
            cfg_analistas.ano = data.year
        else:
            cfg_analistas.ano = DPANO

        if DPMES == None:
            data = date.today()
            cfg_analistas.mes = data.month
        else:
            cfg_analistas.mes = DPMES

        if radio == 'Todos':
            cfg_analistas.analistas = analista()
            page = l_analistas()
            return {'display': 'none'}, page
        else:
            if combo == None:
                return {'display': 'block', 'min-width': '170px', 'margin-left': '20px'}, html.Div()
            else:
                cfg_analistas.analistas = combo
                print(cfg_analistas.analistas)
                page = l_analistas()
                return {'display': 'block', 'min-width': '170px', 'margin-left': '20px'}, page

    return app.server