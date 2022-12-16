import dash_flask.plotlydash.cfg_geral as cfg
from dash_flask.plotlydash.cfg_geral import *
import dash_bootstrap_components as dbc

analistas = []

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

greenBlueYellowOrangeRed = ['', green, blue, yellow, orange, red]

blueYellowOrange = [blue, yellow, orange]

greenRed = [green, red]

ara = [
    "#00a9f8",
    "#00f8ca",
    "#4e00f8",
    "#f800a9",
]


def g_sla(df):
    figura = px.histogram(df, y="ANALISTA", title="ATRIBUIDOS", color='STATUSSLA',
                          text_auto=True, color_discrete_sequence=greenRed, orientation='h', height=700)
    figura.update_xaxes(tickangle=90)
    figura.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_title=None, yaxis_title=None,
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
    figura.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)

    return figura


def g_respostas(df):
    try:
        figura = px.histogram(df, y="ANALISTA", title="RESPOSTAS ANALISTA", color='RANALISTA',
                              text_auto=True, color_discrete_sequence=greenBlueYellowOrangeRed, orientation='h',
                              height=700)
        figura.update_xaxes(tickangle=90)
        figura.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_title=None, yaxis_title=None,
                             paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
        figura.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)

        return figura

    except:

        return g_sem_valores("Sem respostas!")


def analista():
    df = q_chamados_mes()

    analistas = pd.unique(df['ANALISTA'].tolist())
    analistas.sort()

    return analistas


def l_analistas():
    df = q_chamados_mes()
    df = df[df['ANALISTA'].isin(analistas)]
    f_atribuidos = g_sla(df)

    f_resposta = g_respostas(df)

    return [
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Graph(id='example-graph-1', figure=f_atribuidos)
                    , style=estilo
                )
                , width={"size": 12, "order": 1}
            )
        ], className="g-0"),
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Graph(id='example-graph-1', figure=f_resposta)
                    , style=estilo
                )
                , width={"size": 12, "order": 1}
            )
        ], className="g-0"),
    ]
