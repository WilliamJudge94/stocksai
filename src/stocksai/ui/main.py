import streamsync as ss
from stocksai.core.calcs import calculate_annual_returns

# This is a placeholder to get you started or refresh your memory.
# Delete it or adapt it as necessary.
# Documentation is available at https://streamsync.cloud

# Shows in the log when the app starts
# print("Hello world!")


# Its name starts with _, so this function won't be exposed
def _update_message(state):
    is_even = state["counter"] % 2 == 0
    message = "+Even" if is_even else "-Odd"
    state["message"] = message


def decrement(state):
    state["counter"] -= 1
    _update_message(state)


def increment(state):
    state["counter"] += 1
    # Shows in the log when the event handler is run
    print(f"The counter has been incremented.")
    _update_message(state)


# Initialise the state

# "_my_private_element" won't be serialised or sent to the frontend,
# because it starts with an underscore

initial_state = ss.init_state(
    {
        "my_app": {"title": "FIRE Calculator"},
        "_my_private_element": 1337,
        "message": None,
        "counter": 26,
        "annual_returns": {
            "principal_amount": 200_000,
            "monthly_contributions": 6500,
            "stock_price": 100,
            "yearly_stock_increase_pct": 9,
            "investment_years": 30,
            "dividend_yield": 0,
        },
    }
)

_update_message(initial_state)
