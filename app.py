
import streamlit as st

import matplotlib.pyplot as plt
import pandas as pd
#import stockdata as sd
#import black_scholes
import yfinance as yf

from datetime import datetime, timedelta


st.title("Black-Scholes Options Pricing Tool")
st.write("This tool allows you to calculate the price of European call and put options using the Black-Scholes model.")
with st.form("stock_form"):
    ticker = st.text_input("Enter stock ticker (e.g., AAPL):", "")
    submitted = st.form_submit_button("Submit")


if submitted and ticker:
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)

    # Fetch data
    data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))

    if not data.empty:
        st.subheader(f"Closing Price for {ticker.upper()} (Last 30 Days)")
    
       
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data.index.strftime("%m/%d"), data["Close"], label="Close Price", color="green", linewidth=2)
        ax.set_xlabel("Date", color='white')
        ax.set_ylabel("Price (USD)", color='white')
        ax.set_title(f"{ticker.upper()} - Closing Prices", color='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.grid(True, color='white')
        plt.xticks(rotation=45)
        ax.set_facecolor('black')
        fig.patch.set_facecolor('black')

        st.pyplot(fig)
    else:
        st.error("No data found. Check the ticker symbol.")

