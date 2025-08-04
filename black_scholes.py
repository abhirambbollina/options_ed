# black_scholes.py
# This module provides functions to calculate the Black-Scholes option pricing model.
import numpy as np
from scipy.stats import norm
import pandas as pd

def bs_option(S: float, K: float, T: float, r: float, sig: float, type: str) -> float:
    """
    S - stock price
    K - strike price
    T - time to maturity
    r - risk-free interest rate
    sig - implied volatility
    type - "Call" or "Put"

    Returns the price of a European option using the Black-Scholes formula.
    """

    d1 = (np.log(S / K) + (r + 0.5 * sig ** 2) * T) / (sig * np.sqrt(T))
    d2 = d1 - sig * np.sqrt(T)

    if type == "Call":
        price = (S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
    elif type == "Put":
        price = (K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))
    return price


def historical_volatility(data: pd.DataFrame) -> float:
    """
    Calculate historical volatility based on the closing prices in the provided DataFrame.
    """
    log_returns = np.log(data['Close'] / data['Close'].shift(1))
    sig = log_returns.std() * np.sqrt(252)  # Annualize the volatility
    return float(sig.iloc[-1])