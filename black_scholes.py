# black_scholes.py
# This module provides functions to calculate the Black-Scholes option pricing model.
import numpy as np
from scipy.stats import norm
import pandas as pd

def bs_call(S: float, K: float, T: float, r: float, sig: float) -> float:
    """
    S - stock price
    K - strike price
    T - time to maturity
    r - risk-free interest rate
    sig - implied volatility

    Returns the price of a European call option using the Black-Scholes formula.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sig ** 2) * T) / (sig * np.sqrt(T))
    d2 = d1 - sig * np.sqrt(T)
    call_price = (S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))

    return call_price

def bs_put(S: float, K: float, T: float, r: float, sig: float) -> float:
    """
    S - stock price
    K - strike price
    T - time to maturity
    r - risk-free interest rate
    sig - implied volatility

    Returns the price of a European put option using the Black-Scholes formula.
    """
    d1 = (np.log(S / K) + (r + 0.5 * sig ** 2) * T) / (sig * np.sqrt(T))
    d2 = d1 - sig * np.sqrt(T)
    put_price = (K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))

    return put_price

def historical_volatility(data: pd.DataFrame) -> float:
    """
    Calculate historical volatility based on the closing prices in the provided DataFrame.
    """
    log_returns = np.log(data['Close'] / data['Close'].shift(1))
    sig = log_returns.std() * np.sqrt(252)  # Annualize the volatility
    return float(sig.iloc[-1])