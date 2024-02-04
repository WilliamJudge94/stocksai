import pandas as pd
from stocksai.core.calcs import _calculate_annual_returns


def test_calculate_annual_returns():
    # Define the inputs
    principal_amount = 10000.0
    monthly_contributions = 500.0
    stock_price = 100.0
    yearly_stock_increase_pct = 5.0
    investment_years = 2
    dividend_yield = 2.0

    # Call the function with the inputs
    result = _calculate_annual_returns(
        principal_amount,
        monthly_contributions,
        stock_price,
        yearly_stock_increase_pct,
        investment_years,
        dividend_yield,
    )

    # Define the expected output
    expected_output = pd.DataFrame(
        {
            "Year": [1, 2],
            "Start Balance": ["$10,000.00", "$16,700.00"],
            "Shares": [100.0, 159.05],
            "Share Price": [100.0, 105.0],
            "Contrib": ["$6,000.00", "$6,000.00"],
            "Growth": ["$500.00", "$835.00"],
            "Dividends": ["$200.00", "$334.00"],
            "End Balance": [16_700.00, 23_869.00],
        }
    ).set_index("Year")

    # Check if the result matches the expected output
    pd.testing.assert_frame_equal(result, expected_output)
