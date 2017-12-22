"""Utility code."""

import os
import pandas as pd
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
    

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()
