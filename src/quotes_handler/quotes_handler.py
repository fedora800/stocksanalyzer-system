import yfinance as yf
import pandas as pd
import requests
import os
from datetime import datetime

def fetch_sp500_tickers():
    """
    Fetch the list of S&P 500 tickers dynamically from Wikipedia.
    """
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    try:
        # Fetch the page content with SSL verification disabled
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an error for bad status codes
        tables = pd.read_html(response.text)
        sp500_table = tables[0]  # The first table contains the S&P 500 data
        lst_tickers = sp500_table['Symbol'].tolist()
        return lst_tickers
    except Exception as e:
        print(f"Error fetching S&P 500 tickers: {e}")
        return []


def fetch_eod_prices(tickers):
  """
  Fetch the latest EOD prices for the given tickers.
  """
  df_eod_prices = []
  for ticker in tickers:
    try:
      yf_stock = yf.Ticker(ticker)
      #print("Fetching EOD price for ticker = ", ticker, " and the stock = ", yf_stock)
      unsafe_session = requests.session()
      unsafe_session.verify = False
      # yahoo finance API will not allow a lot of requests, i saw that after 50-60 request, it gave below error - 
      # $BKNG: possibly delisted; no price data found  (period=1d)
      df_latest_price = yf_stock.history(period="1d", rounding=True)  # Fetch the latest 1-day df_eod_prices
      #print("df_latest_price", df_latest_price)
      if not df_latest_price.empty:
        latest_close = df_latest_price['Close'].iloc[-1]
        df_eod_prices.append({"Ticker": ticker, "Close": latest_close})
    except Exception as e:
      print(f"Error fetching data for {ticker}: {e}")

  # Create a DataFrame with only the required columns
  return pd.DataFrame(df_eod_prices, columns=["Ticker", "Close"])




# --- main code ---
fil_tickerprices_csv = "sp500_eod_prices.csv"

# Check if the CSV file already exists and is not empty and is not older
if (os.path.exists(fil_tickerprices_csv) and 
  os.path.getsize(fil_tickerprices_csv) > 0 and 
  datetime.fromtimestamp(os.path.getmtime(fil_tickerprices_csv)).date() == datetime.now().date()):
  print(f"The file '{fil_tickerprices_csv}' already exists and is up-to-date (modified today).")
  print(f"Skipping data fetch and loading the csv file into a DataFrame...")
  df_sp500_prices = pd.read_csv(fil_tickerprices_csv)
  print(f"Loaded data = ", df_sp500_prices)
else:
  print(f"The file '{fil_tickerprices_csv}' does not exist or is empty or older than today.")
  # Fetch the tickers
  print(f"Now fetching the list of tickers of the companies in the S&P 500 index")
  lst_sp500_tickers = fetch_sp500_tickers()

  # Display the tickers
  print(lst_sp500_tickers)

  ##lst_sp500_tickers = lst_sp500_tickers[:10]  # Limit to first 10 tickers for testing

  # Fetch EOD prices for S&P 500 tickers
  print(f"Now fetching EOD prices for each of these tickers")
  df_sp500_prices = fetch_eod_prices(lst_sp500_tickers)

  # Display the DataFrame
  print(df_sp500_prices)

  # Save to a CSV file
  print(f"Now saving the EOD prices to CSV file: {fil_tickerprices_csv}")
  df_sp500_prices.to_csv(fil_tickerprices_csv, index=False)
