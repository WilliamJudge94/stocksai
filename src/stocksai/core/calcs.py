import warnings
import pandas as pd
import yfinance as yf
import plotly.express as px

warnings.simplefilter(action="ignore", category=FutureWarning)

pd.set_option("display.float_format", "{:.2f}".format)


def calculate_annual_returns(
    state,
):

    small_state = state["annual_returns"]
    principal_amount = small_state["principal_amount"]
    monthly_contributions = small_state["monthly_contributions"]
    stock_price = small_state["stock_price"]
    yearly_stock_increase_pct = small_state["yearly_stock_increase_pct"]
    investment_years = small_state["investment_years"]
    dividend_yield = small_state["dividend_yield"]

    df = _calculate_annual_returns(
        principal_amount,
        monthly_contributions,
        stock_price,
        yearly_stock_increase_pct,
        investment_years,
        dividend_yield,
    )

    fig = px.line(df, y="End Balance")
    fig.update_layout(yaxis_tickprefix="$", yaxis_tickformat=",.2f")
    fire_number = float(small_state["annual_spend"] / 0.04)
    coast_fire_number = float(small_state["annual_spend"] * 5.85)

    # draw horizontal line for fire number
    fig.add_shape(
        dict(
            type="line",
            x0=1,
            y0=fire_number,
            x1=investment_years,
            y1=fire_number,
            line=dict(color="Red", width=3),
        )
    )

    # draw horizontal line for coast fire number
    fig.add_shape(
        dict(
            type="line",
            x0=1,
            y0=coast_fire_number,
            x1=investment_years,
            y1=coast_fire_number,
            line=dict(color="Green", width=3),
        )
    )

    state["annual_returns"]["fire_number"] = fire_number
    state["annual_returns"]["coast_fire_number"] = coast_fire_number
    # state["annual_returns"]["fire_date"] = find_fire_date
    # state["annual_returns"]["coast_fire_date"] = find_coast_fire_date

    df["End Balance"] = df["End Balance"].map("${:,.2f}".format)
    state["annual_returns"]["df"] = df
    state["annual_returns"]["fig"] = fig


def _calculate_annual_returns(
    principal_amount: float,
    monthly_contributions: float,
    stock_price: float,
    yearly_stock_increase_pct: float,
    investment_years: int,
    dividend_yield: float,
) -> pd.DataFrame:
    """
    Calculate annual investment progress with dividends calculated at the beginning of each year,
    accurately accounting for dividends, reinvestment, and growth to match expected outcomes.

    Parameters
    ----------
    principal_amount : float
        Initial amount invested.
    monthly_contributions : float
        Monthly contribution amount.
    stock_price : float
        Initial stock price per share.
    yearly_stock_increase_pct : float
        Expected annual increase in stock price, as a percentage.
    investment_years : int
        Total number of years for the investment.
    dividend_yield : float
        Annual dividend yield as a percentage of the stock price.

    Returns
    -------
    pd.DataFrame
        DataFrame with yearly investment details: Year, Start Balance, Shares, Share Price,
        Contrib, Growth, Dividends, Reinvested, End Balance.
    """
    records = []
    total_shares = principal_amount / stock_price

    for year in range(1, int(investment_years) + 1):
        start_balance = total_shares * stock_price
        contrib = monthly_contributions * 12
        growth = start_balance * (yearly_stock_increase_pct / 100)
        dividends = total_shares * stock_price * (dividend_yield / 100)
        end_balance = start_balance + contrib + growth + dividends

        records.append(
            {
                "Year": year,
                "Start Balance": start_balance,
                "Shares": total_shares,
                "Share Price": stock_price,
                "Contrib": contrib,
                "Growth": growth,
                "Dividends": dividends,
                "End Balance": end_balance,
            }
        )

        stock_price *= 1 + yearly_stock_increase_pct / 100
        total_shares += (contrib + dividends) / stock_price

    return_df = pd.DataFrame(records).set_index("Year", drop=True)

    # Round specific columns
    return_df[["Shares", "Share Price"]] = return_df[["Shares", "Share Price"]].round(2)

    # Format specified columns as USD
    usd_columns = [
        "Start Balance",
        "Contrib",
        "Growth",
        "Dividends",
    ]
    for col in usd_columns:
        return_df[col] = return_df[col].map("${:,.2f}".format)

    return return_df


def calculate_indicators(
    ticker_symbol="AAPL",
    period="1y",
    interval="1d",
    sma_window=30,
    bb_std_dev=2,
    rsi_window=14,
):
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
        data = stock.history(period=period, interval=interval)
    except Exception as e:
        print(f"An error occurred while fetching the stock data: {e}")
        return None

    # Calculate Simple Moving Average (SMA)
    data[f"{sma_window}d_SMA"] = data["Close"].rolling(window=sma_window).mean()

    # Calculate Bollinger Bands
    data["Upper_BB"] = (
        data[f"{sma_window}d_SMA"]
        + bb_std_dev * data["Close"].rolling(window=sma_window).std()
    )
    data["Lower_BB"] = (
        data[f"{sma_window}d_SMA"]
        - bb_std_dev * data["Close"].rolling(window=sma_window).std()
    )

    # Calculate Relative Strength Index (RSI)
    close_diff = data["Close"].diff(1)
    gains = close_diff.where(close_diff > 0, 0)
    losses = -close_diff.where(close_diff < 0, 0)

    avg_gain = gains.rolling(window=rsi_window).mean()
    avg_loss = losses.rolling(window=rsi_window).mean()

    rs = avg_gain / avg_loss
    data["RSI"] = 100 - (100 / (1 + rs))

    # Normalize the data
    for col in ["Close", f"{sma_window}d_SMA", "Upper_BB", "Lower_BB"]:
        data[col + "_pctchange"] = data[col].pct_change() * 100

    # mean, std = data.RSI.mean(), data.RSI.std()
    # data.RSI = (data.RSI - mean)/std

    return data
