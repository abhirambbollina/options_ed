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
if "r" not in st.session_state:
    st.session_state["r"] = 0.0
if "sig" not in st.session_state:
    st.session_state["sig"] = 0.0
if "option_submitted" not in st.session_state:
    st.session_state["option_submitted"] = False
if "option_type" not in st.session_state:
    st.session_state["option_type"] = "Call"
if "K" not in st.session_state:
    st.session_state["K"] = None
if "T" not in st.session_state:
    st.session_state["T"] = None


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
            st.session_state["r"] = float(yf.Ticker("^TNX").history(period="1d")["Close"].iloc[-1]/100)
            st.session_state["sig"] = bsm.historical_volatility(yf.download(st.session_state["ticker"], period="6mo", interval="1d"))
    else:
        st.error("Please enter a valid ticker.")


if st.session_state["ticker_submitted"] and st.session_state["data"] is not None:
    st.subheader(f"Closing Price for {st.session_state['ticker'].upper()} (Last 30 Days)")

    st.pyplot(scht.stock_plot_30d(st.session_state["ticker"], st.session_state["data"]))

    st.subheader("Black-Scholes Option Pricing")
    
    option_type_input = st.selectbox("Select Option Type:", options=["Call", "Put"])

    S = float(st.session_state["data"]["Close"].iloc[-1])
    r = st.session_state["r"]
    sig = st.session_state["sig"]
    K_input = st.number_input("Strike Price (K):", value=S, step=2.5)
    T_date = st.date_input("Time to Maturity (T):", value=datetime.today() + timedelta(days=30)) 
    T_input = (datetime(T_date.year, T_date.month, T_date.day) - datetime.today()).days / 365.0  # Convert days to years

    if st.button("Calculate Option Price"):
        if K_input >= 0 and T_input > 0 and option_type_input in ["Call", "Put"]:
            st.session_state["option_submitted"] = True
            st.session_state["K"] = K_input
            st.session_state["T"] = T_input
            st.session_state["option_type"] = option_type_input
        else:
            st.error("Invalid input")
            st.session_state["option_submitted"] = False
    
if st.session_state["option_submitted"]:
    K = float(st.session_state["K"])
    T = float(st.session_state["T"])
    option_type = st.session_state["option_type"]
    if option_type == "Call":
        option_price = bsm.bs_call(S, K, T, r, sig)
        st.success(f"The price of the Call Option is: ${option_price:.2f} per share")
    else:
        option_price = bsm.bs_put(S, K, T, r, sig)
        st.success(f"The price of the Put Option is: ${option_price:.2f} per share")
    

    
    





