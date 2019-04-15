"""
Train using prophet time-series model
"""
import logging
import pandas as pd

from fbprophet import Prophet

class TrainProphet:
    """ Train using prophet """

    def __init__(self, df=None, season_mode=None):
        _validate_df(df)
        self._df = df
        self._mode = 'additive' if season_mode is None else 'multiplicative'

        try:
            self._mod = Prophet(seasonality_mode=self._mode)
            self._mod.fit(self._df)
            logging.info("Model initialized with {}".format(self._mode))
        except Exception as e:
            logging.error("Training Error: {}".format(e), exc_info=True)  
            raise
    
    def get_model(self):
        return self._mod
    
    def make_future_dataframe(self, period, freq):
        logging.info("Making future dataframe with {} periods, frequency {}".format(period, freq))
        return self._mod.make_future_dataframe(periods=period, freq=freq)
    
    def get_predictions(self, df):
        logging.info("Predicting...")
        return self._mod.predict(df)


def _validate_df(df):
    if df is None:
        raise TypeError("Pandas Dataframe is required.")
    if len(df.columns) != 2:
        raise ValueError("Number of columns must be 2.")
    if df.columns[0] != 'ds' or df.columns[1] != 'y':
        raise NameError("Column names must be 'ds' and 'y'")
    return
    