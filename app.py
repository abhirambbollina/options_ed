import streamlit as st
import stockchart as scht
import black_scholes as bsm
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

@st.cache_data
def get_stock_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

@st.cache_data
def get_risk_free_rate():
    return float(yf.Ticker("^TNX").history(period="1d")["Close"].iloc[-1] / 100)

@st.cache_data
def get_volatility_data(ticker):
    return yf.download(ticker, period="6mo", interval="1d")

@st.cache_data
def get_expiry_options(ticker):
    return yf.Ticker(ticker).options

@st.cache_resource
def get_option_chain(ticker, expiry_date):
    chain = yf.Ticker(ticker).option_chain(expiry_date)
    return {'calls': chain.calls, 'puts': chain.puts}

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
if "expiry_options" not in st.session_state:
    st.session_state["expiry_options"] = []
if "chain" not in st.session_state:
    st.session_state["chain"] = None


ticker_input = st.text_input("Enter stock ticker (e.g., AAPL):", value=st.session_state["ticker"])
if st.button("Submit"):
    if ticker_input:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=30)

        data = get_stock_data(ticker_input, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

        if data.empty:
            st.error("No data found. Check the ticker symbol.")
            st.session_state["ticker_submitted"] = False
        else:
            st.session_state["ticker"] = ticker_input
            st.session_state["data"] = data
            st.session_state["ticker_submitted"] = True
            st.session_state["r"] = get_risk_free_rate()
            vol_data = get_volatility_data(st.session_state["ticker"])
            st.session_state["sig"] = bsm.historical_volatility(vol_data)
            st.session_state["expiry_options"] = get_expiry_options(ticker_input)
            
    else:
        st.error("Please enter a valid ticker.")


if st.session_state["ticker_submitted"] and st.session_state["data"] is not None:
    st.subheader(f"Closing Price for {st.session_state['ticker'].upper()} (Last 30 Days)")

    st.pyplot(scht.stock_plot_30d(st.session_state["ticker"], st.session_state["data"]))
    st.subheader(f'Current Closing Price: ${float(st.session_state["data"]["Close"].iloc[-1]):.2f}')

    st.header("Black-Scholes Option Pricing")
    
    option_type_input = st.selectbox("Select Option Type:", options=["Call", "Put"])

    

    S = float(st.session_state["data"]["Close"].iloc[-1])
    r = st.session_state["r"]
    sig = st.session_state["sig"]
    
    ticker = st.session_state["ticker"]

    expiry_options = st.session_state["expiry_options"]
    expiry_date = st.selectbox("Select Expiry Date:", options=expiry_options)

    strike_price_options = []
    chain = get_option_chain(ticker, expiry_date)
    st.session_state["chain"] = chain
    if option_type_input == "Call":
        strike_price_options = chain['calls']['strike'].tolist()
    else:
        strike_price_options = chain['puts']['strike'].tolist()

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
    chain = st.session_state["chain"]
    
    
    option_price = bsm.bs_option(S, K, T, r, sig, option_type)
    st.success(f"The price of the Black-Scholes {option_type} Option is: ${option_price:.2f} per share")
    st.write(f"A contract represents 100 shares, the price of a contract is: ${option_price * 100:.2f}")
    if option_type == "Call":
        option_row = chain['calls'][chain['calls']["strike"] == K]
    else:
        option_row = chain['puts'][chain['puts']["strike"] == K]
    st.write(f"Market Prices of {option_type} Option:")
    bid = option_row['bid'].values[0]
    ask = option_row['ask'].values[0]
    mid = (bid + ask) / 2
    st.write(f"Bid: {bid:.2f}")
    st.write(f'Mid: {mid:.2f}')
    st.write(f"Ask: {ask:.2f}")

    st.write("### Price Comparison")
    fig, ax = plt.subplots()
    ax.bar(['Black-Scholes', 'Market Mid'], [option_price, mid])
    ax.set_ylabel('Price ($)')
    ax.set_ylim(bottom=0.1)
    st.pyplot(fig)
    st.write(f"Difference (BS - Market): ${option_price - mid:.2f}")

        

    
    





