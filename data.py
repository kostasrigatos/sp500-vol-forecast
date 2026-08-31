import yfinance as yf
import pandas as pd
from config import TICKERS, EXCLUDE_TICKERS, START_DATE, END_DATE

def fetch_raw_prices(
        tickers: list[str], start: str, end: str, exclude_tickers: list[str] = EXCLUDE_TICKERS
):
    """
    Download OHLCV data for multiple tickers and reshape into a long and tidy format

    Arguments:
    tickers (list) -- list of tickers
    start (str)    -- start date string in YYYY-MM-DD
    end (str)      -- end date string in YYYY-MM-DD
    exclude_tickers (list) -- tickers to exclude due to data starting in 2018 rather than 2010

    Returns:
        pd.DataFrame: a tidied up DataFrame with columns [date, ticker, close, high, low, open, volume]
    """

    # Download the wide multi-index DataFrame
    wide_data = yf.download(tickers, start, end, interval='1d')

    # Stack the 'Ticker' level into the row index; vectorization across all tickers
    long_data = wide_data.stack(level=1)
    # Cleaning of index and column names for SQL
    long_data.index.names = ['date', 'ticker']

    # Column names to lowercase letters and empty spaces to underscores - good SQL practice
    raw_prices = long_data.reset_index()
    raw_prices.columns = raw_prices.columns.str.lower().str.replace(" ", "_")

    # Keep only rows where ticker is NOT the excluded ticker
    raw_prices = raw_prices[~raw_prices["ticker"].isin(exclude_tickers)]

    # Reset the index to keep it continuous after dropping rows
    raw_prices = raw_prices.reset_index(drop=True)

    raw_prices.columns.name = None

    return raw_prices

if __name__ == "__main__":
    df_prices = fetch_raw_prices(TICKERS, START_DATE, END_DATE)

    print(df_prices.head())