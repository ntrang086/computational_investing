"""An example of how to use Capital Asset Pricing Model (CAPM)"""

import numpy as np


def compute_stock_return(alpha, beta, market_return):
    """
    Compute stock return using the CAPM equation
    stock_return = beta * market_return + alpha
    
    Parameters:
    alpha: A measure of the active return on a stock    
    beta: A measure of the risk arising from exposure to general market (e.g. SP500) movements
    market_return: Return rate of the market (e.g. SP500) on a particular day

    Returns: 
    stock_return: Return rate of the stock on a particular day
    """
    stock_return = beta * market_return + alpha
    return stock_return


def compute_portfolio_return(portfolio, weights, alphas, betas, market_return):
    """
    Compute portfolio return using the CAPM equation
    portfolio_return = sum([(stock_beta * market_return + stock_alpha) * stock_weight for each stock in portfolio])
    
    Parameters:
    portfolio: A list of stocks in the portfolio
    weights: A list of weights for stocks in the portfolio
    alphas: A list of betas for stocks in the portfolio
    betas: A list of betas for stocks in the portfolio 
    market_return: Return rate of the market (e.g. SP500) on a particular day

    Returns: 
    portfolio_return: Return rate of the stock on a particular day
    """
    portfolio_return = sum([(betas[i] * market_return + alphas[i]) * weights[i] for i in range(len(weights))])
    return stock_return
