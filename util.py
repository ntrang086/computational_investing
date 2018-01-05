"""Utility code."""

import os
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt


def symbol_to_path(symbol, base_dir=os.path.join("../..", "data")):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates, addSPY=True):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if addSPY and 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols = ['SPY'] + symbols

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col='Date',
                parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)
        if symbol == 'SPY':  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df


def normalize_data(df):
    """Normalize stock prices using the first row of the dataframe"""
    return df/df.iloc[0,:]


def compute_daily_returns(df):
    """Compute and return the daily return values"""
    daily_returns = df.pct_change()
    daily_returns.iloc[0,:] = 0
    return daily_returns


def compute_sharpe_ratio(k, avg_return, risk_free_rate, std_return):
    """
    Compute and return the Sharpe ratio
    Parameters:
    k: adjustment factor, sqrt(252) for daily data, sqrt(52) for weekly data, sqrt(12) for monthly data
    avg_return: daily, weekly or monthly return
    risk_free_rate: daily, weekly or monthly risk free rate
    std_return: daily, weekly or monthly standard deviation
    Returns: 
    sharpe_ratio: k * (avg_return - risk_free_rate) / std_return
    """
    return k * (avg_return - risk_free_rate) / std_return
    

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price", save_fig=False, fig_name="plot.png"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if save_fig == True:
        plt.savefig(fig_name)
    else:
        plt.show()


def load_txt_data(dirpath, filename):
    """ Load the data from a txt file and store them as a numpy array

    Parameters:
    dirpath: The path to the directory where the file is stored
    filename: The name of the file in the dirpath
    
    Returns:
    np_data: A numpy array of the data
    """

    try:
        filepath= os.path.join(dirpath, filename)
    except KeyError:
        print ("The file is missing")

    np_data = np.loadtxt(filepath, dtype=str)

    return np_data


def get_exchange_days(start_date = dt.datetime(1964,7,5), end_date = dt.datetime(2020,12,31),
    dirpath = "../data/dates_lists", filename="NYSE_dates.txt"):
    """ Create a list of dates between start_date and end_date (inclusive) that correspond 
    to the dates there was trading at an exchange. Default values are given based on NYSE.

    Parameters:
    start_date: First timestamp to consider (inclusive)
    end_date: Last day to consider (inclusive)
    dirpath: The path to the directory where the file is stored
    filename: The name of the file in the dirpath
    
    Returns:
    dates: A list of dates between start_date and end_date on which an exchange traded
    """

    # Load a text file located in dirpath
    dates_str = load_txt_data(dirpath, filename)
    all_dates_frome_file = [dt.datetime.strptime(date, "%m/%d/%Y") for date in dates_str]
    df_all_dates = pd.Series(index=all_dates_frome_file, data=all_dates_frome_file)

    selected_dates = [date for date in df_all_dates[start_date:end_date]]

    return selected_dates


def get_data_as_dict(dates, symbols, keys):
    """ Create a dictionary with types of data (Adj Close, Volume, etc.) as keys. Each value is 
    a dataframe with symbols as columns and dates as rows

    Parameters:
    dates: A list of dates of interest
    symbols: A list of symbols of interest
    keys: A list of types of data of interest, e.g. Adj Close, Volume, etc.
    
    Returns:
    data_dict: A dictionary whose keys are types of data, e.g. Adj Close, Volume, etc. and 
    values are dataframes with dates as indices and symbols as columns
    """

    data_dict = {}
    for key in keys:
        df = pd.DataFrame(index=dates)
        for symbol in symbols:
            df_temp = pd.read_csv(symbol_to_path(symbol), index_col="Date",
                    parse_dates=True, usecols=["Date", key], na_values=["nan"])
            df_temp = df_temp.rename(columns={key: symbol})
            df = df.join(df_temp) 
        data_dict[key] = df
    return data_dict
