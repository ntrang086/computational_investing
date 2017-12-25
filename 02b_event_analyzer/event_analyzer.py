import os
import pandas as pd
import numpy as np
import math
import copy
import pickle
import datetime as dt
import matplotlib.pyplot as plt
import sys
# Append the path of the directory one level above the current directory to import util
sys.path.append('../')
from util import *


def detect_return_diff(symbols, data_dict, symbol_change=-0.05, market_change=0.02):
    """ 
    Create the event dataframe. Here we are only interested in the opposite movements of 
    symbol and market, i.e. symbol_change and market_change are of opposite signs

    Parameters:
    symbols: A list of symbols of interest
    data_dict: A dictionary whose keys are types of data, e.g. Adj Close, Volume, etc. and 
    values are dataframes with dates as indices and symbols as columns
    symbol_change: Min.(if positive) or max. (if negative) change in the return of symbol
    market_change: Max.(if negative) or min. (if positive) change in the return of market
    
    Returns:
    df_events: A dataframe filled with either 1's for detected events or NAN's for no events
    """

    df_close = data_dict["Adj Close"]
    market_close = df_close["SPY"]

    # Create a dataframe filled with NAN's
    df_events = copy.deepcopy(df_close)
    df_events = df_events * np.NAN

    # Dates for the event range
    dates = df_close.index

    for symbol in symbols:
        for i in range(1, len(dates)):
            # Calculate the returns for this date
            symbol_return = (df_close[symbol].loc[dates[i]] / df_close[symbol].loc[dates[i - 1]]) - 1
            market_return = (market_close.loc[dates[i]] / market_close.loc[dates[i - 1]]) - 1

            # Event is found if both the symbol and market cross their respective thresholds
            if symbol_change < 0 and market_change > 0:
                if symbol_return <= symbol_change and market_return >= market_change:
                    df_events[symbol].loc[dates[i]] = 1
            elif symbol_change > 0 and market_change < 0:
                if symbol_return >= symbol_change and market_return <= market_change:
                    df_events[symbol].loc[dates[i]] = 1
            else:
                print ("Here we are only interested in the opposite movements of symbol and market, \
                    i.e. you should ensure symbol_change and market_change are of opposite signs")
    return df_events


