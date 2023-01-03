import dash_flask.plotlydash.cfg_geral as cfg
from dash_flask.plotlydash.cfg_geral import *


def info_chart(titulo):
    return html.Div([
        html.H2(titulo, style={"margin-left": "auto", "margin-right": "auto", "color": "white"}),
        html.H1("0", style={"margin-left": "auto", "margin-right": "auto", "color": "white"})
    ], style={"Height": "100%",
              "display": "flex",
              "flex-direction": "column",
              "justify-content": 'center',
              "width": "90%",
              "padding": "10px 0 10px 0",
              "margin-left": "auto",
              "margin-right": "auto",
              'background': 'rgba(20, 20, 20, 1)',
              'border-radius': '16px',
              'box-shadow': '0 2px 10px rgba(0, 0, 0, 0.1)'
              })


def dt_table(df):
    return dash_table.DataTable(df.to_dict('records'),
                                [{"name": i, "id": i} for i in df.columns],
                                style_table={'overflowX': 'auto', 'overflowY': 'auto'},
                                style_cell={'textAlign': 'center', 'border': '0px solid grey'},
                                style_cell_conditional=[
                                    {
                                        'if': {'column_id': 'Region'},
                                        'textAlign': 'center'
                                    }],
                                style_header={
                                    'backgroundColor': 'rgb(30, 30, 30)',
                                    'color': 'white',
                                    'border': '0px solid black',
                                    'fontWeight': 'bold'
                                },
                                style_data={
                                    'backgroundColor': 'rgb(50, 50, 50)',
                                    'color': 'white'
                                },
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(40, 40, 40)',
                                    }],
                                sort_action = 'custom',
                                sort_mode = 'single',
                                sort_by = []
                                )
