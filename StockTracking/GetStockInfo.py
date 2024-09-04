import yfinance as yf

def get_stock_info(ticker):
    """
    Fetches real-time stock information for a given ticker symbol.

    Parameters:
    - ticker (str): The ticker symbol of the stock (e.g., 'AAPL' for Apple).

    Returns:
    - stock_info (dict): A dictionary containing the stock's current price, daily high, low, etc.
    - stock_data_recent: Recent stock data for analysis.
    - stock_data_monthly: Monthly stock data for analysis.
    - stock_data_full: Full stock data for analysis.
    """

    # Download the stock data
    stock = yf.Ticker(ticker)
    stock_data_recent = yf.download(tickers=ticker, period='5d', interval='1m')['Adj Close']  # Gives 1949 rows of data
    stock_data_monthly = yf.download(tickers=ticker, period='1y', interval='1h')['Adj Close']  # Gives 1749 rows of data
    stock_data_full = yf.download(tickers=ticker, period='max', interval='1d')['Adj Close']  # Gives x rows of data

    # Check if data is available
    if stock_data_recent.empty or stock_data_monthly.empty or stock_data_full.empty:
        print(f"No intraday data found for {ticker}")
        return
    
    # Fetch current stock information
    stock_info = stock.info

    # Calculate daily percentage gain
    previous_close = stock_data_recent.iloc[-2]  # Using .iloc for positional indexing
    current_price = stock_data_recent.iloc[-1]   # Using .iloc for positional indexing
    
    # Calculate weekly percentage gain
    last_week_close = stock_data_recent.iloc[0]  # For 5 business days, using .iloc for positional indexing
    weekly_percentage_gain = ((current_price - last_week_close) / last_week_close) * 100
    
    # Extract relevant data
    data = {
        'Ticker': ticker,
        'Company Name': stock_info.get('shortName'),
        'Current Price': current_price,
        'Previous Close': previous_close,
        'Open': stock_info.get('open'),
        'Day High': stock_info.get('dayHigh'),
        'Day Low': stock_info.get('dayLow'),
        '52 Week High': stock_info.get('fiftyTwoWeekHigh'),
        '52 Week Low': stock_info.get('fiftyTwoWeekLow'),
        'Daily Percentage Gain': 100 * (current_price - stock_info.get('open')) / current_price,
        'Weekly Percentage Gain': weekly_percentage_gain
    }
    
    return data, stock_data_recent, stock_data_monthly, stock_data_full

def display_stock_info(stock_info):
    """
    Displays the stock information in a readable format.

    Parameters:
    - stock_info (dict): The stock information dictionary to display.
    """
    print(f"\nStock Information for {stock_info['Company Name']} ({stock_info['Ticker']})")
    print("-" * 50)
    print(f"Current Price           : {stock_info['Current Price']}")
    print(f"Previous Close          : {stock_info['Previous Close']}")
    print(f"Open                    : {stock_info['Open']}")
    print(f"Day High                : {stock_info['Day High']}")
    print(f"Day Low                 : {stock_info['Day Low']}")
    print(f"52 Week High            : {stock_info['52 Week High']}")
    print(f"52 Week Low             : {stock_info['52 Week Low']}")
    print(f"Daily Percentage Gain   : {stock_info['Daily Percentage Gain']:.2f}%")
    print(f"Weekly Percentage Gain  : {stock_info['Weekly Percentage Gain']:.2f}%")

if __name__ == "__main__":
    # Example usage
    tickers = ["AAPL"]
    for ticker in tickers:
        stock_info, _, _, _ = get_stock_info(ticker)
        if stock_info:
            display_stock_info(stock_info)
