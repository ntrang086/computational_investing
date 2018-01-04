"""Bollinger value as a technical indicator"""

import os
import pandas as pd
import matplotlib.pyplot as plt
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


if __name__ == "__main__":
    plot_bollinger("GOOG", dt.datetime(2010, 1, 1), dt.datetime(2010, 12, 31))
