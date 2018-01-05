"""Analyze a portfolio"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import sys
# Append the path of the directory one level above the current directory to import util
sys.path.append('../')
from util import *


def assess_portfolio(sd = dt.datetime(2008,1,1), ed = dt.datetime(2009,1,1), \
    syms = ["GOOG","AAPL","GLD","XOM"], \
    allocs=[0.1,0.2,0.3,0.4], \
    sv=1000000, rfr=0.0, sf=252.0, \
    gen_plot=False):

    """Assess a portfolio by computing statistics

    Parameters:
    sd: A datetime object that represents the start date
    ed: A datetime object that represents the end date
    syms: A list of symbols that make up the portfolio
    allocs: A list of allocations to the stocks, must sum to 1.0
    sv: Start value of the portfolio
    rfr: The risk free return per sample period for the entire date range, assuming it does not change
    sf: Sampling frequency per year
    gen_plot: If True, create a plot named plot.png

    Returns:
    cr: Cumulative return
    adr: Average period return (if sf == 252 this is daily return)
    sddr: Standard deviation of daily return
    sr: Sharpe ratio
    ev: End value of portfolio
    """

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

    # Get daily portfolio value
    port_val = get_portfolio_value(prices, allocs, sv)

    # Get portfolio statistics (sddr == volatility)
    cr, adr, sddr, sr = get_portfolio_stats(port_val, rfr, sf)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # Create a temporary dataframe with both the SPY and Portfolio
        df_temp = pd.concat([port_val, prices_SPY], keys=["Portfolio", "SPY"], axis=1)
        plot_normalized_data(df_temp, title="Daily portfolio and SPY", xlabel="Date", ylabel="Normalized price")    

    # Compute end value
    ev = port_val.ix[-1, 0]

    return cr, adr, sddr, sr, ev


def get_portfolio_value(prices, allocs, sv):
    """Helper function to compute portfolio value

    Parameters:
    prices: Adjusted closing prices for portfolio symbols
    allocs: A list of allocations to the stocks, must sum to 1.0
    sv: Start value of the portfolio
    
    Returns:
    port_val: A dataframe object showing the portfolio value for each day
    """

    # Normalize the prices according to the first day
    norm_prices = normalize_data(prices)

    # Compute prices based on the allocations
    alloc_prices = norm_prices * allocs

    # Calculate position values
    pos_vals = alloc_prices * sv

    # Get daily portfolio value
    port_val = pos_vals.sum(axis=1).to_frame()

    return port_val


def get_portfolio_stats(port_val, daily_rf, samples_per_year):
    """Helper function to compute portfolio statistics

    Parameters:
    port_val: A dataframe object showing the portfolio value for each day
    daily_rf: Daily risk-free rate, assuming it does not change
    samples_per_year: Sampling frequency per year
    
    Returns:
    cr: Cumulative return
    adr: Average daily return
    sddr: Standard deviation of daily return
    sr: Sharpe ratio
    """
    cr = port_val.iloc[-1, 0]/port_val.iloc[0, 0] - 1

    daily_returns = compute_daily_returns(port_val)[1:]
    adr = daily_returns.iloc[:, 0].mean()
    sddr = daily_returns.iloc[:, 0].std()
    sr = compute_sharpe_ratio(np.sqrt(samples_per_year), adr, daily_rf, sddr)

    return cr, adr, sddr, sr


def plot_normalized_data(df, title, xlabel, ylabel, save_fig=False, fig_name="plot.png"):
    """Helper function to normalize and plot data"""

    # Normalize the data
    df = normalize_data(df)

    # Plot the normalized data
    plot_data(df, title=title, xlabel=xlabel, ylabel=ylabel, save_fig=save_fig, fig_name=fig_name)


def test_code():
    # Define input parameters
    start_date = dt.datetime(2010,1,1)
    end_date = dt.datetime(2010,12,31)
    symbols = ["GOOG", "AAPL", "GLD", "XOM"]
    allocations = [0.2, 0.3, 0.4, 0.1]
    start_val = 1000000  
    risk_free_rate = 0.0
    sample_freq = 252

    # Assess the portfolio
    cr, adr, sddr, sr, ev = assess_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        allocs = allocations,\
        sv = start_val, \
        gen_plot = True)

    # Print statistics
    print ("Start Date:", start_date)
    print ("End Date:", end_date)
    print ("Symbols:", symbols)
    print ("Allocations:", allocations)
    print ("Sharpe Ratio:", sr)
    print ("Volatility (stdev of daily returns):", sddr)
    print ("Average Daily Return:", adr)
    print ("Cumulative Return:", cr)
    print ("End value:", ev)

if __name__ == "__main__":
    test_code()
