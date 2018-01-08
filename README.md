# Computational investing

There are two parts:

1 Compute stock return using Capital Asset Pricing Model (CAPM)

2 Projects:

a) Market simulator: Read in an orders file that contains trade orders (buy and sell), compute a portfolio value for all the trades and other statistics and compare the portfolio's performance with that of $SPX

b) Technical analysis: Implement a basic technical indicator and an advanced one (Bollinger value) to detect events of interest, plot them and output events as trades to be fed into a market simulator

## Setup

You need Python 2.7+, and the following packages: pandas, numpy, scipy and matplotlib.


## Data

Data files can be downloaded from [this link](http://quantsoftware.gatech.edu/images/a/af/ML4T_2017Fall.zip) or from [Yahoo Finance](https://finance.yahoo.com/)

Place the data into a directory named 'data' and it should be one level above this repository.

## Run

To run any script file, use:

```bash
python <script.py>
```

Source: [Part 2](http://quantsoftware.gatech.edu/Computational_Investing) of [Machine Learning for Trading](http://quantsoftware.gatech.edu/Machine_Learning_for_Trading_Course) by Georgia Tech
