from dash_flask.plotlydash import cfg_trimestral

from dash_flask.plotlydash.cfg_trimestral import *


def init_trimestral(server):
    app = Dash(server=server, routes_pathname_prefix="/trimestral/", external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = html.Div(children=[

        dbc.Row([
            html.Div([
                html.Img(src="../static/assets/logo-stefanini-preto.svg", style={'width': '150px', 'height': '50px'}),
                html.Div([
                    html.Div(
                        dcc.RadioItems(['Trimestral', 'Mensal'], id='radio', style={'width': '100px'}),
                        style={'width': '200px'}
                    ),

                    html.Div(
                        dcc.Dropdown(lista_ano(), placeholder='ANO', id='DPANO'),
                        style={'width': '100%', 'margin-right': '5%'}
                    ),

                    html.Div(
                        dcc.Dropdown(lista_mes(), placeholder='MES', id='DPMES'), id='COMBOMES',
                        style={'width': '100%', 'margin-right': '5%'}
                    )
                ], style={'display': 'flex', 'align-items': 'center', 'margin-left': 'auto'})
            ], style={
                'display': 'flex',
                'background-color': '#99CCFF',
                'align-items': 'center',
                'justify-content': 'flex-start',
                'position': 'fixed',
                'z-index': '1',
                'height': '60px'
            })

        ], className="g-0"),
        html.Div(id='layout', style={'background-color': '#1c1d21', 'margin-top': '60px'}),
        html.Div(id='teste')
    ])

    @callback(
        Output('COMBOMES', component_property='children'),
        Input(component_id='radio', component_property='value')
    )
    def build_graph(radio):
        if radio == 'Trimestral':
            return dcc.Dropdown(lista_trimestral(), placeholder='MES', id='DPMES', style={'width': '100%'})
        else:
            return dcc.Dropdown(lista_mes(), placeholder='MES', id='DPMES', style={'width': '100%'})

    @callback(
        Output('layout', component_property='children'),
        Input('DPMES', component_property='value')
    )
    def layout(input_value):
        print(input_value)
        if input_value is None:
            data = date.today()
            input_value = data.month
            print(input_value)

        if len(str(input_value)) > 2:
            mesInicio = str(input_value[0]) + str(input_value[1])
            mesFim = str(input_value[-2]) + str(input_value[-1])
            html = l_chamados(mesInicio, mesFim)
            return html
        else:
            html = l_chamados(input_value, input_value)
            return html

    @callback(
        Output('comboanalista', component_property='children'),
        Input(component_id='radio', component_property='value')
    )
    def change_combo(radio):
        return radio

    return app.server