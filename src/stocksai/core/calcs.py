import pandas as pd
import plotly.express as px

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

    state["annual_returns"]["df"] = df

    state["annual_returns"]["fig"] = px.line(df, y="End Balance")


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

    for year in range(1, investment_years + 1):
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
