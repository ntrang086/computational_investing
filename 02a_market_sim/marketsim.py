"""Market simulator"""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    """
    Parameters:
    orders_file: The name of a file from which to read orders; may be a string, or a file object
    start_val: The starting value of the portfolio (initial cash available)
    commission: The fixed amount in dollars charged for each transaction (both entry and exit)
    impact: The amount the price moves against the trader compared to the historical data at each transaction
    
    Returns:
    portvals: A dataframe with one column containing the value of the portfolio for each trading day
    """

    # In the template, instead of computing the value of the portfolio, we just
    # read in the value of IBM over 6 months
    #portvals = pd.DataFrame.from_csv(orders_file)
    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])

    # Sort the orders_df by index, i.e the date column
    orders_df.sort_index(ascending=True, inplace=True)
    
    start_date = orders_df.index.min()
    end_date = orders_df.index.max()
    symbols = orders_df.Symbol.unique()

    # Create a dataframe with adjusted close prices for the symbols
    df_prices = get_data(symbols, pd.date_range(start_date, end_date), addSPY=False)
    df_prices.dropna(inplace=True)

    # Add a column for adjusted close price for cash, which is $1
    df_prices["cash"] = 1.0
    #print (df_prices)

    # Create a dataframe that represents changes in the number of shares by day for each asset. 
    # It has the same structure as df_prices, and is initially filled with zeros
    df_trades = pd.DataFrame(np.zeros((df_prices.shape)), df_prices.index, df_prices.columns)
    #print (orders_df)
    for index, row in orders_df.iterrows():
        if row["Order"] == "BUY":
            df_trades.loc[index, row["Symbol"]] = row["Shares"]
            df_trades.loc[index, "cash"] = df_prices.loc[index, row["Symbol"]] * row["Shares"] * (-1.0)
        else:
            df_trades.loc[index, row["Symbol"]] = -row["Shares"]
            df_trades.loc[index, "cash"] = df_prices.loc[index, row["Symbol"]] * row["Shares"]

    # Create a dataframe that represents on each particular day how much of each asset we are holding
    # It has the same structure as df_prices, and is initially filled with zeros
    df_holdings = pd.DataFrame(np.zeros((df_prices.shape)), df_prices.index, df_prices.columns)
    for row_count in range(len(df_holdings)):
        if row_count == 0:
            df_holdings.iloc[0, :-1] = df_trades.iloc[0, :-1].copy()
            df_holdings.iloc[0, -1] = df_trades.iloc[0, -1] + start_val
        else:
            df_holdings.iloc[row_count] = df_holdings.iloc[row_count-1] + df_trades.iloc[row_count]
        row_count += 1

    # Dummy portvals
    portvals = pd.DataFrame(index=df_prices.index, data=df_prices.iloc[:, 0].as_matrix())
    print (portvals)

    return portvals


def test_code():
    # This is a helper function to test the above code
    
    # Define input parameters
    of = "./orders/orders-short.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    print (portvals)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    start_date = dt.datetime(2011,1,10)
    end_date = dt.datetime(2011,12,20)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print ("Date Range: {} to {}".format(start_date, end_date))
    print ()
    print ("Sharpe Ratio of Fund: {}".format(sharpe_ratio))
    print ("Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY))
    print ()
    print ("Cumulative Return of Fund: {}".format(cum_ret))
    print ("Cumulative Return of SPY : {}".format(cum_ret_SPY))
    print ()
    print ("Standard Deviation of Fund: {}".format(std_daily_ret))
    print ("Standard Deviation of SPY : {}".format(std_daily_ret_SPY))
    print ()
    print ("Average Daily Return of Fund: {}".format(avg_daily_ret))
    print ("Average Daily Return of SPY : {}".format(avg_daily_ret_SPY))
    print ()
    print ("Final Portfolio Value: {}".format(portvals[-1]))

if __name__ == "__main__":
    test_code()
