from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import pyodbc
from datetime import date

data = date.today()
ano = data.year
mes = data.month

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


def conectar():
    SERVER_NAME = 'SOALV3SQLPROD,1438'
    DATABASE_NAME = 'dbEAcesso'

    return pyodbc.connect("""
            Driver={{SQL Server Native Client 11.0}};
            Server={0};
            Database={1};
            Trusted_Connection=yes;""".format(SERVER_NAME, DATABASE_NAME))


def q_chamados_mes():
    conn = conectar()
    sql_query = f"""
select
	c.id,
	CASE
		when GRUPOATRIBUIDO = 'OPERACAO - N1' then 'N1'
		WHEN GRUPOATRIBUIDO = 'SISTEMAS CORPORATIVOS' then 'N2'
	END AS GRUPOATRIBUIDO
	,CASE
		WHEN STATUSSLA = 'Within SLA' THEN 'NO SLA'
		WHEN STATUSSLA = 'Breached SLA' THEN 'FORA SLA'
	END AS STATUSSLA
	,CASE
		WHEN UPPER(SUBSTRING(c.CATEGORIZACAO, 1, CHARINDEX(' ', c.CATEGORIZACAO) - 1)) = 'NULL' THEN 'SEM CATEGORIA'
		WHEN UPPER(SUBSTRING(c.CATEGORIZACAO, 1, CHARINDEX(' ', c.CATEGORIZACAO) - 1)) = 'SISTEMAS' THEN 'STFCORP'
		WHEN UPPER(SUBSTRING(c.CATEGORIZACAO, 1, CHARINDEX(' ', c.CATEGORIZACAO) - 1)) = 'INFORME' THEN 'INF. RENDIMENTOS'
		WHEN UPPER(SUBSTRING(c.CATEGORIZACAO, 1, CHARINDEX(' ', c.CATEGORIZACAO) - 1)) = 'PESQUISA' THEN 'PESQ. CANDIDATO'
		ELSE UPPER(SUBSTRING(c.CATEGORIZACAO, 1, CHARINDEX(' ', c.CATEGORIZACAO) - 1))
	END AS CATEGORIZACAO
	,CONCAT (SUBSTRING(atribuid, 1, CHARINDEX(' ', atribuid) - 1),' ',reverse (SUBSTRING(reverse(atribuid), 1, CHARINDEX(' ', reverse(atribuid)) - 1))) AS ANALISTA	
	,MES = MONTH(DTCRIACAO)
	,CASE
		WHEN MONTH(DTCRIACAO) = 1 THEN 'JAN'
		WHEN MONTH(DTCRIACAO) = 2 THEN 'FEV'
		WHEN MONTH(DTCRIACAO) = 3 THEN 'MAR'
		WHEN MONTH(DTCRIACAO) = 4 THEN 'ABR'
		WHEN MONTH(DTCRIACAO) = 5 THEN 'MAI'
		WHEN MONTH(DTCRIACAO) = 6 THEN 'JUN'
		WHEN MONTH(DTCRIACAO) = 7 THEN 'JUL'
		WHEN MONTH(DTCRIACAO) = 8 THEN 'AGO'
		WHEN MONTH(DTCRIACAO) = 9 THEN 'SET'
		WHEN MONTH(DTCRIACAO) = 10 THEN 'OUT'
		WHEN MONTH(DTCRIACAO) = 11 THEN 'NOV'
		WHEN MONTH(DTCRIACAO) = 11 THEN 'DEZ'
	END AS MESEXTENSO,
	CASE
		WHEN C.ID IN (SELECT ID FROM TBLCHAMADOSPESQUISA) THEN P.RESPOSTA
		ELSE NULL
	END AS RSERVICO,
	CASE
		WHEN C.ID IN (SELECT ID FROM TBLCHAMADOSPESQUISA) THEN P2.RESPOSTA
		ELSE NULL
	END AS RANALISTA,
	CASE
		WHEN C.ID IN (SELECT ID FROM TBLCHAMADOSPESQUISA) THEN 'SIM'
		ELSE 'NÃO'
	END AS RESPONDIDO

from TBLCHAMADOS c

left join DBEACESSO..TBLCHAMADOSPESQUISA p on c.ID = p.id AND p.PERGUNTA = 'Qual o nível de satisfação em relação a entrega dos serviços deste chamado?'
left join DBEACESSO..TBLCHAMADOSPESQUISA p2 on c.ID = p2.id AND p2.PERGUNTA = 'Qual é o nível de satisfação com a atuação do PO ou Analista?'

where 
	GRUPOATRIBUIDO in('SISTEMAS CORPORATIVOS','OPERACAO - N1')
	and c.CATEGORIZACAO not like'%causa%'
    and YEAR(DTCRIACAO)={ano} and MONTH(DTCRIACAO)>={mes} and MONTH(DTCRIACAO)<={mes}
	and ATRIBUID NOT IN ('Thiago  De Campos Madeira', 'Izabel  Pereira De Jesus', 'Bruna  Ferreira De Paula', 'Ricardo  Januario Calabria', 'Niedja  Farias Neves Da Silva', 'Bruno  Santiago Primola De Souza')
	and c.STATUS IN ('CLOSED', 'Resolved-Validation')
	and STATUSSLA not in ('SLA Not Applied')         
ORDER BY STATUSSLA DESC, CASE WHEN P2.RESPOSTA = 'Ótimo' THEN 1
		      WHEN P2.RESPOSTA = 'Bom' THEN 2
		      WHEN P2.RESPOSTA = 'Regular' THEN 3
		      WHEN P2.RESPOSTA = 'Ruim' THEN 4
		      WHEN P2.RESPOSTA = 'Péssimo' THEN 5
		END
    """
    df = pd.read_sql(sql_query, conn)
    conn.close()

    return df


def q_reabertos():
    conn = conectar()
    sql_query = f"""
        select MONTH(dtabertura) as MES from TBLCHAMADOSREABERTOS where ANALISTA NOT IN ('Thiago De Campos Madeira', 'Izabel Pereira De Jesus', 'Bruna Ferreira De Paula', 'Ricardo Januario Calabria', 'Niedja Farias Neves Da Silva')
        AND GRUPO NOT IN ('BACKOFFICE', 'FECHAMENTO')
        AND YEAR(DTABERTURA)=2022 and MONTH(DTABERTURA) >= {mes} and MONTH(DTABERTURA) <= {mes}
    """

    df = pd.read_sql(sql_query, conn)
    conn.close()
    return df


def g_sla(df):
    figura = px.histogram(df, y="ANALISTA", title="ATRIBUIDOS", color='STATUSSLA',
                          text_auto=True, color_discrete_sequence=greenRed, orientation='h', height=700)
    figura.update_xaxes(tickangle=90)
    figura.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_title=None, yaxis_title=None,
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
    figura.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)

    return figura


def g_respostas(df):
    figura = px.histogram(df, y="ANALISTA", title="RESPOSTAS ANALISTA", color='RANALISTA',
                          text_auto=True, color_discrete_sequence=greenBlueYellowOrangeRed, orientation='h', height=700)
    figura.update_xaxes(tickangle=90)
    figura.update_layout(yaxis={'categoryorder': 'total ascending'}, xaxis_title=None, yaxis_title=None,
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')
    figura.update_traces(textfont_size=12, textangle=0, textposition="inside", cliponaxis=False)

    return figura


def lista_mes():
    data = date.today()
    qtdmes = data.month
    meses = []
    for mes in range(qtdmes):
        if data.year == 2022 and mes >= 3:
            meses.append(str(mes + 1))

    return meses


def lista_ano():
    data = date.today()
    qtdano = data.year
    anos = []

    while qtdano >= 2022:
        anos.append(qtdano)
        qtdano -= 1

    return anos


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