"""Test for optimization.py"""


from marketsim import compute_portvals
import unittest
import math
import pandas as pd
from analysis import get_portfolio_stats


class TestMarketSimWithOrders(unittest.TestCase):

    def test_compute_portvals(self):
        orders_file = "./orders/orders.csv"
        portvals = compute_portvals(orders_file)

        # Check if portvals is a dataframe
        self.assertTrue(isinstance(portvals, pd.DataFrame))

        # Test portfolio stats
        cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals, daily_rf=0.0, samples_per_year=252.0)
        self.assertTrue(math.isclose(cum_ret, 0.108872698544, rel_tol=0.02), "Cumulative return is incorrect")
        self.assertTrue(math.isclose(avg_daily_ret, 0.000459098655493, rel_tol=0.02), "Average daily return is incorrect")
        self.assertTrue(math.isclose(std_daily_ret, 0.00730509916835, rel_tol=0.02), "Standard deviation is incorrect")
        self.assertTrue(math.isclose(sharpe_ratio, 0.997654521878, rel_tol=0.02), "Sharpe ratio is incorrect")
        self.assertTrue(math.isclose(portvals.iloc[-1, -1], 1106025.8065, rel_tol=0.02), "Portfolio value is incorrect")


class TestMarketSimWithOrders2(unittest.TestCase):

    def test_compute_portvals(self):
        orders_file = "./orders/orders2.csv"
        portvals = compute_portvals(orders_file)

        # Check if portvals is a dataframe
        self.assertTrue(isinstance(portvals, pd.DataFrame))

        # Test portfolio stats
        cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = get_portfolio_stats(portvals, daily_rf=0.0, samples_per_year=252.0)
        self.assertTrue(math.isclose(cum_ret, 0.0538411196951, rel_tol=0.02), "Cumulative return is incorrect")
        self.assertTrue(math.isclose(avg_daily_ret, 0.000253483085898, rel_tol=0.02), "Average daily return is incorrect")
        self.assertTrue(math.isclose(std_daily_ret, 0.00728172910323, rel_tol=0.02), "Standard deviation is incorrect")
        self.assertTrue(math.isclose(sharpe_ratio, 0.552604907987, rel_tol=0.02), "Sharpe ratio is incorrect")
        self.assertTrue(math.isclose(portvals.iloc[-1, -1], 1051088.0915, rel_tol=0.02), "Portfolio value is incorrect")    
    

if __name__ == '__main__':
    unittest.main()