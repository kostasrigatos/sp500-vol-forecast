import yfinance as yf
import pandas as pd
# from datetime import datetime --- uncomment this if you want end_date to fetch the latest live data

def fetch_raw_prices(
        tickers: list[str], start: str, end: str, exclude_tickers: list[str] = ["XLC", "XLRE"]
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
    tickers = ['XLK', 'XLF', 'XLE', 'XLV', 'XLY', 'XLP', 'XLI', 'XLB', 'XLU', 'XLRE', 'XLC', 'SPY']
    start_date = '2010-01-01'
    end_date = '2026-08-31'  # for live data instead: end_date = use datetime.today().strftime("%Y-%m-%d")

    df_prices = fetch_raw_prices(tickers, start_date, end_date)