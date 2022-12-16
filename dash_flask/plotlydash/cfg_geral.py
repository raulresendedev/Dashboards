from datetime import date
import plotly.express as px
import tracemalloc
from dash_flask.plotlydash.cfg_bd import q_reabertos, q_chamados_mes
from dash import Dash, dcc, html, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc

tracemalloc.start()

data = date.today()
ano = data.year
mes_inicio = data.month
mes_fim = data.year


def lista_mes():
    qtdmes = data.month
    meses = []
    for mes in range(qtdmes):
        if data.year == 2022 and mes >= 3:
            meses.append(str(mes + 1))

    return meses


def lista_trimestral():
    trimestres = []

    if ano == 2022 or ano == '2022':
        trimestres = ['04 05 06', '07 06 09', '10 11 12']
        return trimestres

    if data.month == 1 or data.month == 2 or data.month == 3:
        trimestres = ['01 02 03']

    elif data.month == 4 or data.month == 5 or data.month == 6:
        trimestres = ['01 02 03', '04 05 06']

    elif data.month == 7 or data.month == 8 or data.month == 9:
        trimestres = ['01 02 03', '04 05 06', '07 06 09']

    elif data.month == 10 or data.month == 11 or data.month == 12:
        trimestres = ['01 02 03', '04 05 06', '07 06 09', '10 11 12']

    return trimestres


def lista_ano():
    qtdano = data.year
    anos = []

    while qtdano >= 2022:
        anos.append(qtdano)
        qtdano -= 1
    return anos


def g_sem_valores(title):
    data = [title, [0], [0]]

    figura = px.histogram(title=data[0], y=data[1], x=data[2])

    figura.update_layout(xaxis_title=None, yaxis_title=None,
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template='plotly_dark')

    return figura


def verifica_consumo():

    current, peak = tracemalloc.get_traced_memory()
    # tracemalloc.stop()
    print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
