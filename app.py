import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import stockchart as scht
import black_scholes
import yfinance as yf
from datetime import datetime, timedelta

st.title("Black-Scholes Options Pricing Tool")
st.write("This tool allows you to calculate the price of European call and put options using the Black-Scholes model.")


if "ticker" not in st.session_state:
    st.session_state["ticker"] = ""
if "data" not in st.session_state:
    st.session_state["data"] = None
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False


ticker_input = st.text_input("Enter stock ticker (e.g., AAPL):", value=st.session_state["ticker"])
if st.button("Submit"):
    if ticker_input:
        end_date = datetime.today()
        start_date = end_date - timedelta(days=30)

        data = yf.download(ticker_input, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

        if data.empty:
            st.error("No data found. Check the ticker symbol.")
            st.session_state["submitted"] = False
        else:
            # Store in session_state
            st.session_state["ticker"] = ticker_input
            st.session_state["data"] = data
            st.session_state["submitted"] = True
    else:
        st.error("Please enter a valid ticker.")


if st.session_state["submitted"] and st.session_state["data"] is not None:
    st.subheader(f"Closing Price for {st.session_state['ticker'].upper()} (Last 30 Days)")
    st.pyplot(scht.stock_plot_30d(st.session_state["ticker"], st.session_state["data"]))

    





