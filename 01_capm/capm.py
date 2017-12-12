"""An example of how to use Capital Asset Pricing Model (CAPM)"""


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


def compute_portfolio_return(weights, alphas, betas, market_return):
    """
    Compute portfolio return using the CAPM equation
    portfolio_return = sum([(stock_beta * market_return + stock_alpha) * stock_weight for each stock in portfolio])
    
    Parameters:
    weights: A list of weights for stocks in the portfolio
    alphas: A list of betas for stocks in the portfolio
    betas: A list of betas for stocks in the portfolio 
    market_return: Return rate of the market (e.g. SP500) on a particular day

    Returns: 
    portfolio_return: Return rate of the stock on a particular day
    """
    portfolio_return = sum([(betas[i] * market_return + alphas[i]) * weights[i] for i in range(len(weights))])
    return portfolio_return


def compute_portfolio_return2(weights, stock_returns):
    """
    Compute portfolio return when having weights and stock returns
    portfolio_return = sum([stock_return * stock_weight for each stock in portfolio])
    
    Parameters:
    weights: A list of weights for stocks in the portfolio
    stock_returns: A list of returns for stocks in the portfolio

    Returns: 
    portfolio_return: Return rate of the stock on a particular day
    """
    portfolio_return = sum([weights[i] * stock_returns[i] for i in range(len(weights))])
    return portfolio_return


def test_run():
    """ Example of a portfolio with two stocks
    stock_A: predict +1% over market, i.e. alpha_A == 1%
    beta_A == 1.0
    $50 long position in stock A
    
    stock_B: predict -1% below market, i.e. alpha_B == -1%
    beta_A == 2.0
    $50 short position in stock B
    """
    alpha_A = 0.01
    beta_A = 1.0
    position_A = 50.0

    alpha_B = -0.01
    beta_B = 2.0
    position_B = -50.0

    market_return = 0.1

    # Calculate stock A return
    return_A = compute_stock_return(alpha_A, beta_A, market_return)
    return_B = compute_stock_return(alpha_B, beta_B, market_return)
    return_A_dollar = return_A * position_A
    return_B_dollar = return_B * position_B

    portfolio_return = compute_portfolio_return([0.5, -0.5], [alpha_A, alpha_B], [beta_A, beta_B], market_return)
    try:
        assert (portfolio_return == compute_portfolio_return2([0.5, -0.5], [return_A, return_B]))
    except AssertionError:
        print ("We have a problem with compute_stock_return")

    print ("Stock A's return in % = {:.0%}, in dollars = {}".format(return_A, return_A_dollar))
    print ("Stock B's return in % = {:.0%}, in dollars = {}".format(return_B, return_B_dollar))
    print ("Portfolio return in % = {:.0%}, in dollars = {}".format(portfolio_return, return_A_dollar + return_B_dollar))

    
if __name__ == "__main__":
    test_run()
