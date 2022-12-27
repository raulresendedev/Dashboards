import dash_flask.plotlydash.cfg_geral as cfg
from dash_flask.plotlydash.cfg_geral import *

def dt_table():
   df = q_aging()
   return dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])