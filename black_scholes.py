# black_scholes.py
# This module provides functions to calculate the Black-Scholes option pricing model.
import math
from scipy.stats import norm

def bs_call(S: float, K: float, T: float, r: float, sig: float) -> float:
    """
    S - stock price
    K - strike price
    T - time to maturity
    r - risk-free interest rate
    sig - implied volatility

    Returns the price of a European call option using the Black-Scholes formula.
    """
    d1 = (math.log(S / K) + (r + 0.5 * sig ** 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    call_price = (S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2))

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
    d1 = (math.log(S / K) + (r + 0.5 * sig ** 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    put_price = (K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))

    return put_price