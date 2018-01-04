"""Bollinger value as a technical indicator"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import copy
import sys
# Append the path of the directory one level above the current directory to import util
sys.path.append("../")
from util import *
from event_analyzer import output_events_as_trades, plot_events


def get_bollinger_bands(rolling_mean, rolling_std, num_std=2):
    """
    Calculate upper and lower Bollinger Bands

    Parameters:
    rolling_mean: Rolling mean of a series
    rolling_meanstd: Rolling std of a series
    num_std: Number of standard deviations for the bands

    Returns: Bollinger upper band and lower band
    """
    upper_band = rolling_mean + rolling_std * num_std
    lower_band = rolling_mean - rolling_std * num_std
    return upper_band, lower_band


def compute_bollinger_value(price, rolling_mean, rolling_std):
    """
    Output a value indicating how many standard deviations a price is from the mean

    Parameters:
    price: Price, typically adjusted close price, series of a symbol
    rolling_mean: Rolling mean of a series
    rolling_std: Rolling std of a series

    Returns:
    bollinger_val: the number of standard deviations a price is from the mean
    """

    bollinger_val = (price - rolling_mean) / rolling_std
    return bollinger_val


def plot_bollinger(symbol, start_date, end_date, window=20, num_std=1):
    """
    Plot Bollinger bands and value for a symbol

    Parameters:
    symbol: A symbol of interest
    start_date: First timestamp to consider (inclusive)
    end_date: Last day to consider (inclusive)rolling_mean: Rolling mean of a series
    window: Number of days to look back for rolling_mean and rolling_std
    num_std: Number of standard deviations for the bands

    Returns:
    Plot two subplots, one for the Adjusted Close Price and Bollinger bands, the other 
    for the Bollinger value
    """

    # Get NYSE trading dates
    dates = get_exchange_days(start_date, end_date, dirpath="../../data/dates_lists", 
        filename="NYSE_dates.txt")

    # Get stock data
    df_price = get_data([symbol], dates)

    # Compute rolling mean
    rolling_mean = df_price[symbol].rolling(window=window).mean()

    # Compute rolling standard deviation
    rolling_std = df_price[symbol].rolling(window=window).std()

    # Compute Bollinger bands and value
    upper_band, lower_band = get_bollinger_bands(rolling_mean, rolling_std, num_std)
    bollinger_val = compute_bollinger_value(df_price[symbol], rolling_mean, rolling_std)
    
    # Create 2 subplots
    # First subplot: symbol's adjusted close price, rolling mean and Bollinger Bands
    f, ax = plt.subplots(2, sharex=True)
    ax[0].fill_between(upper_band.index, upper_band, lower_band, color="gray", alpha=0.4, 
        linewidth=2.0, label="Region btwn Bollinger Bands")
    ax[0].plot(df_price[symbol], label=symbol + " Adjusted Close", color="b")
    ax[0].set_title("{} Adjusted Close with Bollinger Bands (num. of std = {})".format(
        symbol, num_std))
    ax[0].set_ylabel("Adjusted Close Price")
    ax[0].legend(loc="upper center")

    # Second subplot: the bollinger value
    ax[1].axhspan(-num_std, num_std, color="gray", alpha=0.4, linewidth=2.0,
        label="Region btwn {} & {} std".format(-num_std, num_std))
    ax[1].plot(bollinger_val, label=symbol + " Bollinger Value", color="b")
    ax[1].set_title("{} Bollinger Value)".format(symbol))
    ax[1].set_xlabel("Date")
    ax[1].set_ylabel("Bollinger Value")
    ax[1].set_xlim(bollinger_val.index.min(), bollinger_val.index.max())
    ax[1].legend(loc="upper center")
    plt.show()


def detect_bollinger(symbols, data_dict, window=20, 
    symbol_bv_change=-2.0, market_bv_change=1.0):
    """ 
    Create the event dataframe based on changes in Bollinger values. Here we are only 
    interested in the opposite movements of symbol and market, i.e. symbol_bv_change 
    and market_bv_change are of opposite signs

    Parameters:
    symbols: A list of symbols of interest
    data_dict: A dictionary whose keys are types of data, e.g. Adj Close, Volume, etc. and 
    values are dataframes with dates as indices and symbols as columns
    window: Number of days to look back for rolling_mean and rolling_std
    symbol_bv_change: Change in the Bollinger value of symbol
    market_bv_change: Change in the Bollinger value of market
    
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

    # Compute rolling mean for market
    market_rm = market_close.rolling(window=window).mean()

    # Compute rolling standard deviation for market
    market_rstd = market_close.rolling(window=window).std()

    # Compute Bollinger value for market
    market_bv = compute_bollinger_value(market_close, market_rm, market_rstd)

    for symbol in symbols:
        # Compute rolling mean for symbol
        symbol_rm = df_close[symbol].rolling(window=window).mean()

        # Compute rolling standard deviation for symbol
        symbol_rstd = df_close[symbol].rolling(window=window).std()

        # Compute Bollinger value for symbol
        symbol_bv = compute_bollinger_value(df_close[symbol], symbol_rm, symbol_rstd)

        for i in range(window, len(dates)):
            # Get the Bollinger values today and yesterday
            symbol_bv_yesterday = symbol_bv.loc[dates[i - 1]]
            symbol_bv_today = symbol_bv.loc[dates[i]]
            market_bv_today = market_bv.loc[dates[i]]

            # Event is found if both the symbol and market cross their respective thresholds
            if symbol_bv_change < 0 and market_bv_change > 0:
                if symbol_bv_yesterday >= symbol_bv_change and \
                symbol_bv_today <= symbol_bv_change and market_bv_today >= market_bv_change:
                    df_events[symbol].loc[dates[i]] = 1
            elif symbol_bv_change > 0 and market_bv_change < 0:
                if symbol_bv_yesterday <= symbol_bv_change and \
                symbol_bv_today >= symbol_bv_change and market_bv_today <= market_bv_change:
                    df_events[symbol].loc[dates[i]] = 1
            else:
                print ("Here we are only interested in the opposite movements of symbol and market, \
                    i.e. you should ensure symbol_bv_change and market_bv_change are of opposite signs")
    return df_events


if __name__ == "__main__":
    # Plot Bollinger bands and values for Google
    plot_bollinger("GOOG", dt.datetime(2010, 1, 1), dt.datetime(2010, 12, 31))

    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    dates = get_exchange_days(start_date, end_date, dirpath="../../data/dates_lists", 
        filename="NYSE_dates.txt")

    symbols = load_txt_data(dirpath="../../data/symbols_lists", filename="sp5002012.txt").tolist()
    symbols.append("SPY")

    keys = ["Open", "High", "Low", "Adj Close", "Volume", "Close"]
    data_dict = get_data_as_dict(dates, symbols, keys)

    # Fill NAN values if any
    for key in keys:
        data_dict[key] = data_dict[key].fillna(method="ffill")
        data_dict[key] = data_dict[key].fillna(method="bfill")
        data_dict[key] = data_dict[key].fillna(1.0)

    # Detect events
    df_events = detect_bollinger(symbols, data_dict)

    # Plot means and standard deviations of events
    plot_events(df_events, data_dict, num_backward=20, num_forward=20,
                output_filename="bollinger_event_chart.pdf", market_neutral=True, error_bars=True,
                market_sym="SPY")
    
