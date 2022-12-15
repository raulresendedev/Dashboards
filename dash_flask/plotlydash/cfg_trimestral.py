from dash import Dash, dcc, html, Output, Input, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash_flask.plotlydash.cfg_bd import q_reabertos, q_chamados_mes

estilo = {
    'background': 'rgba(20, 20, 20, 1)',
    'border-radius': '16px',
    'box-shadow': '0 2px 10px rgba(0, 0, 0, 0.1)',
    'margin': '10px',
    'color': 'white'
}

labelStyle = {
    'margin-left': 'auto',
    'margin-right': 'auto',
    'margin-bottom': '0px',
    'width': 'fit-content',
    'height': 'fit-content'
}

green = '#01F777'
red = '#E73C3C'
blue = '#5351fc'
yellow = '#EEF500'
orange = '#FF8900'

greenBlueYellowOrangeRed = [green, blue, yellow, orange, red]

blueYellowOrange = [blue, yellow, orange]

greenRed = [green, red]

ara = [
    "#00a9f8",
    "#00f8ca",
    "#4e00f8",
    "#f800a9",
]





def g_sla_total(df):
    figura = px.pie(df, names='STATUSSLA', title="SLA TOTAL", hole=.5, color_discrete_sequence=greenRed,
                    template='plotly_dark')
    figura.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return figura


def porcentagem(valor, total):
    if valor == 0:
        return 0
    else:
        return round((valor / total) * 100, 1)


def g_sla_mes(df):

    mesesExt = pd.unique(df['MESEXTENSO'].tolist())

    noSla = []
    foraSla = []

    for mes in mesesExt:
        qtdNoSla = len(df[(df['STATUSSLA'] == 'NO SLA') & (df['MESEXTENSO'] == mes)])
        qtdFora = len(df[(df['STATUSSLA'] == 'FORA SLA') & (df['MESEXTENSO'] == mes)])
        qtdTotal = qtdNoSla + qtdFora
        noSla.append(porcentagem(qtdNoSla, qtdTotal))
        foraSla.append(porcentagem(qtdFora, qtdTotal))

    figura = px.bar(x=mesesExt, y=[noSla, foraSla], text_auto=True, title='META SLA', color_discrete_sequence=greenRed)
    figura.add_hline(y=90, line_width=1, fillcolor=red, opacity=1)
    figura.update_traces(width=.4)
    figura.update_yaxes(range=[60, 100])
    figura.update_layout(showlegend=False)
    figura.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
    figura.update_layout(xaxis_title=None, yaxis_title=None, uniformtext_minsize=8, uniformtext_mode='hide')
    return figura


def g_reabertos(df_r, df_c):

    mesesExt = pd.unique(df_c['MESEXTENSO'].tolist())
    meses = pd.unique(df_c['MES'].tolist())
    qtdReabertos = []
    qtdRestante = []

    for i, mes in enumerate(mesesExt):
        c = df_c['MESEXTENSO'].value_counts()[mes]
        r = df_r['MES'].value_counts()[meses[i]]
        qtdReabertos.append(porcentagem(r, c))
        qtdRestante.append(100 - qtdReabertos[i])


    figura = px.bar(x=mesesExt, y=[qtdRestante, qtdReabertos], title="CHAMADOS REBERTOS", text_auto=True, color_discrete_sequence=greenRed)
    figura.update_traces(width=.4)
    figura.update_yaxes(range=[90, 100])
    figura.update_layout(showlegend=False)
    figura.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
    figura.update_layout(xaxis_title=None, yaxis_title=None)

    return figura


def g_atribuidos(df):
    figura = px.histogram(df, x="ANALISTA", title="ATRIBUIDOS", barmode="group", color='MESEXTENSO', height=500,
                          text_auto=True, color_discrete_sequence=ara)
    figura.update_xaxes(tickangle=90)
    figura.update_layout(xaxis={'categoryorder': 'total descending'}, xaxis_title=None, yaxis_title=None,
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
    figura.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    return figura


def g_categorizacao(df):
    figura = px.histogram(df, x="CATEGORIZACAO", title="CATEGORIZAÇÃO", color='GRUPOATRIBUIDO', barmode="group",
                          text_auto=True, color_discrete_sequence=ara)
    figura.update_layout(xaxis={'categoryorder': 'total descending'}, xaxis_title=None, yaxis_title=None)
    figura.update_xaxes(tickangle=90)
    figura.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
    figura.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    return figura


def g_grupos(df):
    figura = px.histogram(df, x='GRUPOATRIBUIDO', color='STATUSSLA', text_auto=True, title="SLA POR GRUPO",
                          color_discrete_sequence=greenRed)
    figura.update_layout(xaxis={'categoryorder': 'total descending'}, xaxis_title=None, yaxis_title=None,
                         uniformtext_minsize=8, uniformtext_mode='hide')
    figura.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
    return figura


def g_grupo_atribuido(df):
    figura = px.histogram(df, x='ANALISTA', color='GRUPOATRIBUIDO', text_auto=True, barmode="group",
                          title="GRUPOS POR ANALISTA", color_discrete_sequence=ara)
    figura.update_layout(xaxis={'categoryorder': 'total descending'}, xaxis_title=None, yaxis_title=None)
    figura.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    figura.update_xaxes(tickangle=90)
    figura.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
    return figura


def g_pesquisa_analista(df):
    df2 = df.dropna(how='any', axis=0)
    figura = px.pie(df2, names='RANALISTA', title="PESQUISA ANALISTA", hole=.5,
                    color_discrete_sequence=greenBlueYellowOrangeRed)
    figura.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
    return figura


def g_pesquisa_servico(df):
    df2 = df.dropna(how='any', axis=0)
    figura = px.pie(df2, names='RSERVICO', title="PESQUISA SERVICO", hole=.5,
                    color_discrete_sequence=greenBlueYellowOrangeRed)
    figura.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
    return figura


def g_total_respostas(df):
    figura = px.pie(df, names='RESPONDIDO', title="RESPONDIDO", hole=.5, color_discrete_sequence=[red, green])
    figura.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
    return figura


def nps_pesquisa(df, coluna):
    promotor = 0
    detrator = 0
    total = 0

    df2 = df.dropna(how='any', axis=0)

    for resposta in df2[coluna]:
        if resposta == 'Ótimo' or resposta == 'Bom':
            promotor += 1
        elif resposta == 'Péssimo' or resposta == 'Ruim':
            detrator += 1
        total += 1

    try:
        porcentagemP = porcentagem(promotor, total)
        porcentagemD = porcentagem(detrator, total)

        nps = round((porcentagemP - porcentagemD), 2)
    except:
        nps = "Sem respostas"

    return str(nps)


def quantidade_chamados(df):
    stringChamados = ''
    meses = pd.unique(df['MESEXTENSO'].tolist())

    for mes in meses:
        stringChamados += str(mes) + " - " + str(df['MESEXTENSO'].value_counts()[mes]) + ' | '

    if len(meses) > 1:
        stringChamados += 'TOTAL - ' + str(len(df['MESEXTENSO']))
    else:
        stringChamados = stringChamados.replace(' | ', '')

    return stringChamados


def quantidade_sla(df):
    noSla = df['STATUSSLA'].value_counts()['NO SLA']
    foraSla = df['STATUSSLA'].value_counts()['FORA SLA']

    return 'NO SLA: ' + str(noSla) + " | FORA DO SLA: " + str(foraSla)


def l_chamados():
    df_chamados = q_chamados_mes()

    df_reabertos = q_reabertos()

    g_sla_total1 = g_sla_total(df_chamados)

    g_atribuidos1 = g_atribuidos(df_chamados)

    g_categorizacao1 = g_categorizacao(df_chamados)

    g_sla_mes1 = g_sla_mes(df_chamados)

    g_grupos1 = g_grupos(df_chamados)

    g_grupo_atribuido1 = g_grupo_atribuido(df_chamados)

    g_pesquisa_analista1 = g_pesquisa_analista(df_chamados)

    g_pesquisa_servico1 = g_pesquisa_servico(df_chamados)

    g_total_respostas1 = g_total_respostas(df_chamados)

    g_reabertos1 = g_reabertos(df_reabertos, df_chamados)

    return [
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='example-graph-1', figure=g_sla_total1),
                    html.Hr(style={'margin': '0px'}),
                    html.H5(quantidade_sla(df_chamados), style=labelStyle)
                    ], style=estilo),
                width={"size": 4, "order": 1}
            ),
            dbc.Col(
                html.Div(
                    dcc.Graph(id='example-graph-2', figure=g_sla_mes1)
                    , style=estilo),
                width={"size": 4, "order": "last"},
            ),
            dbc.Col(
                html.Div(
                    dcc.Graph(id='example-graph-2', figure=g_reabertos1)
                    , style=estilo),
                width={"size": 4, "order": "last"},
            )
        ], className="g-0"),

        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='example-graph-3', figure=g_atribuidos1),
                    html.Hr(style={'margin': '0px'}),
                    html.H5(quantidade_chamados(df_chamados), style=labelStyle)
                ], style=estilo),
                width={"size": 12, "order": 1}
            ),
        ], className="g-0"),

        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Graph(id='example-graph-5', figure=g_grupos1)
                    , style=estilo),
                width={"size": 3, "order": 1}
            ),
            dbc.Col(
                html.Div(
                    dcc.Graph(id='example-graph-6', figure=g_grupo_atribuido1)
                    , style=estilo),
                width={"size": 9, "order": 1}
            ),
        ], className="g-0"),

        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Graph(id='example-graph-4', figure=g_categorizacao1)
                    , style=estilo),
                width={"size": 12, "order": 1},
            ),
        ], className="g-0"),

        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='exampl', figure=g_total_respostas1),
                    html.Hr(style={'margin': '0px'}),
                    html.H5('RESPOSTAS: ' + str(len(df_chamados.dropna(how='any', axis=0))), style=labelStyle)
                ], style=estilo),
                width={"size": 4, "order": 1},
            ),

            dbc.Col(
                html.Div([
                    dcc.Graph(id='example', figure=g_pesquisa_analista1),
                    html.Hr(style={'margin': '0px'}),
                    html.H5('NPS: ' + nps_pesquisa(df_chamados, 'RANALISTA'), style=labelStyle)
                ], style=estilo),
                width={"size": 4, "order": 1},
            ),

            dbc.Col(
                html.Div([
                    dcc.Graph(id='exampl', figure=g_pesquisa_servico1),
                    html.Hr(style={'margin': '0px'}),
                    html.H5('NPS: ' + nps_pesquisa(df_chamados, 'RSERVICO'), style=labelStyle)
                ], style=estilo),
                width={"size": 4, "order": 1},
            )

        ], className="g-0"),
    ]