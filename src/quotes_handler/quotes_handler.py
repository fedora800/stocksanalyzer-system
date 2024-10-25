# streamlit app basic template with docker 
import os
import yfinance as yf
import pandas as pd


def main():
  app_version = os.getenv('APP_VERSION')
  print('APP_VERSION = ', app_version)

  
  # Get the S&P 500 constituents
  table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
  sp500_constituents = table[0]['Symbol'].tolist()

  # Get yesterday's closing prices
  yesterday = pd.to_datetime('today') - pd.DateOffset(days=1)
  closing_prices = []

  for ticker in sp500_constituents:
      try:
          ticker_data = yf.download(ticker, start=yesterday, end=yesterday)
          closing_price = ticker_data['Close'].iloc[0]
          closing_prices.append((ticker, closing_price))
      except Exception as e:
          print(f"Error downloading data for {ticker}: {e}")

  # Create a DataFrame with the closing prices
  df = pd.DataFrame(closing_prices, columns=['Ticker', 'Closing Price'])
  print(df)


if __name__ == '__main__':
    main()




