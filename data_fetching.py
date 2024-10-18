import yfinance as yf
import pandas as pd
from datetime import timedelta

def fetch_crypto_data_multiple(tickers: list, start_date: str, end_date: str) -> dict:
    """
    Fetches historical cryptocurrency data for multiple tickers over a specified period.

    Parameters:
    tickers (list): A list of cryptocurrency ticker symbols.
    start_date (str): The start date for fetching data (e.g., '2022-01-01').
    end_date (str): The end date for fetching data (e.g., '2024-01-01').

    Returns:
    dict: A dictionary containing historical cryptocurrency data for each ticker.
    """
    crypto_data = {}
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if data.empty:
                print(f"No data found for ticker: {ticker}")
            else:
                crypto_data[ticker] = data
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
    
    return crypto_data

def split_into_quarters(crypto_data: pd.DataFrame) -> dict:
    """
    Splits the cryptocurrency data into quarters.

    Parameters:
    crypto_data (pd.DataFrame): The historical data for a single cryptocurrency.

    Returns:
    dict: A dictionary where keys are the quarter names and values are DataFrames for that quarter.
    """
    quarters = {}
    start_year = crypto_data.index[0].year
    end_year = crypto_data.index[-1].year
    
    for year in range(start_year, end_year + 1):
        for q in range(1, 5):
            start_month = 3 * (q - 1) + 1
            end_month = start_month + 3
            quarter_name = f"Q{q}-{year}"
            quarter_data = crypto_data.loc[f"{year}-{start_month:02d}":f"{year}-{end_month - 1:02d}"]
            if not quarter_data.empty:
                quarters[quarter_name] = quarter_data
    return quarters

def display_quarterwise_data(crypto_data_dict: dict):
    """
    Displays cryptocurrency data split by quarters for each ticker.

    Parameters:
    crypto_data_dict (dict): Dictionary containing cryptocurrency data for multiple tickers.
    """
    for ticker, data in crypto_data_dict.items():
        print(f"\n--- {ticker} ---")
        quarters = split_into_quarters(data)
        for quarter, quarter_data in quarters.items():
            print(f"\n{quarter}:\n{quarter_data[['Close']].head()}")  # Displaying first few rows for each quarter

if __name__ == "__main__":
    # Define multiple cryptocurrency tickers
    tickers = ["BTC-USD", "ETH-USD"]  # Bitcoin and Ethereum
    start_date = "2020-01-01"
    end_date = "2024-01-01"
    
    # Fetch data for multiple tickers
    crypto_data_dict = fetch_crypto_data_multiple(tickers, start_date, end_date)
    
    # Display quarterwise data for each ticker
    display_quarterwise_data(crypto_data_dict)
