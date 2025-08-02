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
    st.subheader(f"Current Closing Price: ${float(st.session_state["data"]["Close"].iloc[-1]):.2f}")

    st.header("Black-Scholes Option Pricing")
    
    option_type_input = st.selectbox("Select Option Type:", options=["Call", "Put"])

    

    S = float(st.session_state["data"]["Close"].iloc[-1])
    r = st.session_state["r"]
    sig = st.session_state["sig"]
    
    ticker = st.session_state["ticker"]

    expiry_options = yf.Ticker(ticker).options
    expiry_date = st.selectbox("Select Expiry Date:", options=expiry_options)

    strike_price_options = []
    chain = yf.Ticker(ticker).option_chain(expiry_date)
    if option_type_input == "Call":
        strike_price_options = chain.calls['strike'].tolist()
    else:
        strike_price_options = chain.puts['strike'].tolist()

    closest_strike_index = strike_price_options.index(min(strike_price_options, key=lambda x: abs(x - S)))
    
    T = (datetime.strptime(expiry_date, "%Y-%m-%d") - datetime.today()).days / 365.0 
    K = st.selectbox("Select Strike Price:", options=strike_price_options, index=closest_strike_index)

    if st.button("Calculate Option Price"):
        if K and T and option_type_input:
            st.session_state["option_submitted"] = True
            st.session_state["K"] = K
            st.session_state["T"] = T
            st.session_state["option_type"] = option_type_input
        else:
            st.error("Invalid input")
            st.session_state["option_submitted"] = False
    
if st.session_state["option_submitted"]:
    K = float(st.session_state["K"])
    T = float(st.session_state["T"])
    option_type = st.session_state["option_type"]
    if option_type == "Call":
        call_row = chain.calls[chain.calls["strike"] == K]
        option_price = bsm.bs_call(S, K, T, r, sig)
        st.success(f"The price of the Black-Scholes Call Option is: ${option_price:.2f} per share")
        st.write(f"Market Mid Price of Call Option: {(call_row["bid"].values[0] + call_row["ask"].values[0]) / 2:.2f} per share")
    else:
        put_row = chain.puts[chain.puts["strike"] == K]
        option_price = bsm.bs_put(S, K, T, r, sig)
        st.success(f"The price of the Black-Scholes Put Option is: ${option_price:.2f} per share")
        st.write(f"Market Mid Price of Put Option: {(put_row['bid'].values[0] + put_row['ask'].values[0]) / 2:.2f} per share")
    

    
    





