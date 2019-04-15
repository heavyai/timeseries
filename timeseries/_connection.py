"""
Connection to omnisci core
"""

import logging
import time

import pymapd

from _querybuilder import QueryBuilder

class Connection:
    """ Connect to omnisci-core """

    def __init__(self, username=None, password=None, dbname=None, port=6274, host=None, protocol=None, querybuilder=None):
       self._username = "mapd" if username is None else username
       self._password = "HyperInteractive" if password is None else password
       self._dbname = "mapd" if dbname is None else dbname
       self._port = port
       self._host = "172.17.0.1" if host is None else host
       self._protocol = "binary" if protocol is None else protocol
       if querybuilder is None:
           raise ValueError("QueryBuilder is required.") 
       self._querybuilder = querybuilder
       
       try:
           self._conn = pymapd.connect(user=self._username, password=self._password, host=self._host, dbname=self._dbname, protocol=self._protocol, port=self._port)
           logging.info("Successfully established connection: {}".format(self._conn))
       except Exception as e:
            logging.error("Connection Error: {}".format(e), exc_info=True)  
            raise
    
    @property
    def connection(self):
        return self._conn

    def close(self):
        self._conn.close()
        logging.info("Closing connection.")
    
    def extract_results(self):
        """ Extract results in pandas """

        try:
            st = time.time()
            it = self._conn.execute(self._querybuilder.query)
            logging.info("Time taken to extract results: {}".format(time.time() - st))
        except Exception as e:
            logging.error("Failed to extract results: {}".format(e), exc_info=True)
            raise
        return it

    def _ddl(self, ntable):
        _drop = "DROP table if exists {}".format(ntable)
        col = 'TIMESTAMP' if self._querybuilder._ts else 'DATE'
        _create = "CREATE table {}(ds {}, trend double, yhat_lower double, yhat_upper double, trend_lower double, trend_upper double, additive_terms double, additive_terms_lower double, additive_terms_upper double, multiplicative_terms double, multiplicative_terms_lower double, multiplicative_terms_upper double, yhat double)".format(ntable, col)
        try:
            self._conn.execute(_drop)
            self._conn.execute(_create)
            logging.info("Successfully created table {}.".format(ntable))
        except Exception as e:
            logging.error("Failed to execute create/drop statements: {}".format(e), exc_info=True)
            raise

    def store_predictions(self, df):
        """Stores predictions in DB"""
        ntable = self._querybuilder.pred_table_name
        self._ddl(ntable)
        try:
            df = df[['ds','trend', 'yhat_lower', 'yhat_upper', 'trend_lower', 'trend_upper', 'additive_terms', 'additive_terms_lower', 'additive_terms_upper','multiplicative_terms', 'multiplicative_terms_lower', 'multiplicative_terms_upper', 'yhat']]
            st = time.time()
            self._conn.load_table_columnar(ntable, df, preserve_index=False)
            logging.info("Time taken to load results: {}".format(time.time() - st))
        except Exception as e:
            logging.error("Failed to load table: {}".format(e), exc_info=True)
            raise
        
        return ntable
        