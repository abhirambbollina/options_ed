import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd



def stock_data_30d(ticker: str) -> pd.DataFrame:
    """
    Returns a pandas dataframe for the pas 30 days of given ticker.
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)

    start_str = start_date.strftime('%Y-%m-%d')
    end_str = end_date.strftime('%Y-%m-%d')

    data = yf.download("AAPL", start=start_str, end=end_str)
    return data


