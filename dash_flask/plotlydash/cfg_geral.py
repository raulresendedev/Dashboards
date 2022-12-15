from datetime import date


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

    if ano == 2022:
        trimestres = ['04 05 06', '07 06 09', '10 11 12']
        return trimestres

    elif data.month == 1 or data.month == 2 or data.month == 3:
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