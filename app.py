import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import stockchart as scht
import black_scholes as bsm
import yfinance as yf
from datetime import datetime, timedelta

st.title("Black-Scholes Options Pricing Tool")
st.write("This tool allows you to calculate the price of European call and put options using the Black-Scholes model.")

#session state variables
if "ticker" not in st.session_state:
    st.session_state["ticker"] = ""
if "data" not in st.session_state:
    st.session_state["data"] = None
if "ticker_submitted" not in st.session_state:
    st.session_state["ticker_submitted"] = False


ticker_input = st.text_input("Enter stock ticker (e.g., AAPL):", value=st.session_state["ticker"])
if st.button("Submit"):
    if ticker_input:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=30)

        data = yf.download(ticker_input, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

        if data.empty:
            st.error("No data found. Check the ticker symbol.")
            st.session_state["ticker_submitted"] = False
        else:
            st.session_state["ticker"] = ticker_input
            st.session_state["data"] = data
            st.session_state["ticker_submitted"] = True
    else:
        st.error("Please enter a valid ticker.")


if st.session_state["ticker_submitted"] and st.session_state["data"] is not None:
    st.subheader(f"Closing Price for {st.session_state['ticker'].upper()} (Last 30 Days)")

    st.pyplot(scht.stock_plot_30d(st.session_state["ticker"], st.session_state["data"]))

    st.subheader("Black-Scholes Option Pricing")
    
    # Historical volatility calculation
    
    S = float(st.session_state["data"]["Close"].iloc[-1])
    r = float(yf.Ticker("^TNX").history(period="1d")["Close"].iloc[-1]/100)
    sig = bsm.historical_volatility(yf.download(st.session_state["ticker"], period="6mo", interval="1d"))

    K = float(st.number_input("Strike Price (K):", value=float(S), step=2.5))
    T = float(st.number_input("Time to Maturity (in years):", value=1.0, step=0.01))
    

    if st.button("Calculate Call Option Price"):
        call_price = bsm.bs_call(S, K, T, r, sig)
        st.success(f"Call Option Price: ${call_price:.2f} per share")

    if st.button("Calculate Put Option Price"):
        put_price = bsm.bs_put(S, K, T, r, sig)
        st.success(f"Put Option Price: ${put_price:.2f}  per share")


    
    





