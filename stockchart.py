import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd




def stock_plot_30d(ticker: str, data: pd.DataFrame) -> plt.Figure:
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
    return fig


