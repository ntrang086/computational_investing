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
