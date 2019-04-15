"""
Build query from parameters
"""

import logging

class QueryBuilder:
    """ Build sql query """

    def __init__(self, date=None, ts=False, response=None, table=None, where=None, groupby=False, having=None, limit=None):
        if all(n is None for n in [date, ts]):
           raise TypeError("One of date/timestamp column name is required.")
        if response is None:
            raise TypeError("Response column name is required.")
        if table is None:
            raise TypeError("Table name is required.")
        
        self._ds = date if ts is False else "CAST({} AS TIMESTAMP(0))".format(date)
        self._y = response
        self._ts = ts
        self._table = table
        self._pred_table = table+"_forecast"
        self._where = None if where == 'None' else where
        self._groupby = groupby
        self._having = None if having == 'None' else having
        self._limit = None if limit == 'None' else limit

        query = "SELECT {} as ds, {} as y FROM {}".format(self._ds, self._y, self._table)
        if not _has_conditions(self._where, self._groupby, self._having, self._limit):
            self._query = query
        else:
            if self._where is not None:
                query += " where {}".format(self._where)
            if self._groupby:
                query += " group by ds"
            if self._having is not None:
                query += " having {}".format(self._having)
            if self._limit is not None:
                query += " limit {}".format(self._limit)
            
            self._query = query

        logging.info("Generated query is: '{}'.".format(query))

    @property
    def table_name(self):
        return self._table
    
    @property
    def pred_table_name(self):
        return self._pred_table

    @property
    def query(self):
        """ Generate sql query """
        return self._query

def _has_conditions(where, groupby, having, limit):
    if all(con is None for con in [where, groupby, having, limit]):
        return False
    return True

