# from datetime import datetime --- uncomment this if you want end_date to fetch the latest live data

TICKERS = ['XLK', 'XLF', 'XLE', 'XLV', 'XLY', 'XLP', 'XLI', 'XLB', 'XLU', 'XLRE', 'XLC', 'SPY']
EXCLUDE_TICKERS = ["XLC", "XLRE"]
START_DATE = '2010-01-01'
END_DATE = '2026-08-31'  # for live data instead: END_DATE = use datetime.today().strftime("%Y-%m-%d")

DB_PATH = 'sector_vol.db'
