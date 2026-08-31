import sqlite3
import pandas as pd
from config import TICKERS, EXCLUDE_TICKERS, START_DATE, END_DATE, DB_PATH

def save_to_db(
        df: pd.DataFrame, db_name: str, table_name: str
):
    """
    Write a pandas DataFrame to an SQLite database table
    """
    # Create the connection to the new SQLite database file
    connection = sqlite3.connect(db_name)

    # Write the DataFrame 'raw_prices' to the database
    df.to_sql(table_name, connection, if_exists='replace', index=False)

    # Close the connection
    connection.close()


if __name__ == "__main__":
    from data import fetch_raw_prices

    save_to_db(fetch_raw_prices(TICKERS, START_DATE, END_DATE), DB_PATH, 'raw_prices')