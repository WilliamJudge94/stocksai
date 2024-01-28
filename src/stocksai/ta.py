import warnings
import yfinance as yf

warnings.simplefilter(action='ignore',
                      category=FutureWarning)

def calculate_indicators(ticker_symbol='AAPL',
                         period='1y',
                         interval='1d',
                         sma_window=30,
                         bb_std_dev=2,
                         rsi_window=14):
    
    """
    Calculate the Simple Moving Average (SMA), Bollinger Bands, and Relative Strength Index (RSI) for a given stock.

    Parameters:
    ticker_symbol (str): The ticker symbol of the stock.
    period (str): The time period for fetching historical data.
    interval (str): The interval for fetching historical data.
    sma_window (int): The window size for calculating SMA.
    bb_std_dev (int): The standard deviation for calculating Bollinger Bands.
    rsi_window (int): The window size for calculating RSI.

    Returns:
    DataFrame: A DataFrame with columns for Close, SMA, Upper Bollinger Band, Lower Bollinger Band, and RSI.
    """
    try:
        # Fetch historical stock data
        stock = yf.Ticker(ticker_symbol)
        data = stock.history(period=period,
                             interval=interval)
    except Exception as e:
        print(f"An error occurred while fetching the stock data: {e}")
        return None

    # Calculate Simple Moving Average (SMA)
    data[f'{sma_window}d_SMA'] = data['Close'].rolling(window=sma_window).mean()

    # Calculate Bollinger Bands
    data['Upper_BB'] = data[f'{sma_window}d_SMA'] + bb_std_dev * data['Close'].rolling(window=sma_window).std()
    data['Lower_BB'] = data[f'{sma_window}d_SMA'] - bb_std_dev * data['Close'].rolling(window=sma_window).std()

    # Calculate Relative Strength Index (RSI)
    close_diff = data['Close'].diff(1)
    gains = close_diff.where(close_diff > 0, 0)
    losses = -close_diff.where(close_diff < 0, 0)

    avg_gain = gains.rolling(window=rsi_window).mean()
    avg_loss = losses.rolling(window=rsi_window).mean()

    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1 + rs))


    # Normalize the data
    for col in ['Close', f'{sma_window}d_SMA', 'Upper_BB', 'Lower_BB']:
        data[col + '_pctchange'] = data[col].pct_change() * 100

    # mean, std = data.RSI.mean(), data.RSI.std()
    # data.RSI = (data.RSI - mean)/std

    return data