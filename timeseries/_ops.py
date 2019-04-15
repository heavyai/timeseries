"""
Perform time series analysis
"""

import logging
import time

from _querybuilder import QueryBuilder
from _connection import Connection
from _prophet import TrainProphet

import pandas as pd

def apply_forecast_impl(params):
    if len(params) < 11:
        raise ValueError("Insufficient number of parameters provided.")
    
    date = str(params[0]).strip()
    y = str(params[1]).strip()
    table = str(params[2]).strip()
    ts = str(params[3]).strip() == 'True'
    where = str(params[4]).strip() 
    groupby = str(params[5]).strip() == 'True'
    having = str(params[6]).strip()
    limit = str(params[7]).strip()
    season_mode = str(params[8]).strip()
    period = int(str(params[9]).strip())
    freq = str(params[10]).strip()

    try:
        qb = QueryBuilder(date=date, response=y, table=table, ts=ts, where=where, groupby=groupby, having=having, limit=limit)
        
        con = Connection(querybuilder=qb)
        it = con.extract_results()
        df = pd.DataFrame(list(it), columns=['ds', 'y'])

        prof = TrainProphet(df, season_mode=season_mode)
        future = prof.make_future_dataframe(period=period, freq=freq)
        preds = prof.get_predictions(future)
        con.store_predictions(preds)
        con.close()
        return qb.pred_table_name
    except Exception as e:
        logging.error("Error processing request: {}.".format(e))
        return str(e)
