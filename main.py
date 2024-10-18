import pandas as pd
from data_fetching import fetch_crypto_data_multiple, display_quarterwise_data
from trading_strategy import apply_moving_average_strategy, apply_risk_management, backtest_strategy
from metrics import print_performance_metrics  # Import the metrics module

import warnings
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

def hyperparameter_tuning(crypto_data: pd.DataFrame):
    """
    Performs hyperparameter tuning for the moving average strategy.

    Parameters:
    crypto_data (pd.DataFrame): Historical price data for the cryptocurrency.
    
    Returns:
    dict: The best parameters and the associated cumulative return.
    """
    best_return = float('-inf')
    best_params = {}

    # Define the parameter grid
    param_grid = {
        'short_window': range(10, 31, 5),  # Testing short windows from 10 to 30
        'long_window': range(50, 101, 10),  # Testing long windows from 50 to 100
        'stop_loss': [0.03, 0.05, 0.07],  # Stop loss percentages
        'take_profit': [0.05, 0.10, 0.15]  # Take profit percentages
    }

    # Iterate through all combinations of parameters

    best_results = None
    for short_window in param_grid['short_window']:
        for long_window in param_grid['long_window']:
            for stop_loss in param_grid['stop_loss']:
                for take_profit in param_grid['take_profit']:
                    # Apply the moving average strategy
                    strategy_data = apply_moving_average_strategy(crypto_data, short_window, long_window)
                    # Apply risk management
                    strategy_data = apply_risk_management(strategy_data, stop_loss, take_profit)
                    # Backtest the strategy
                    results = backtest_strategy(strategy_data)

                    # Check cumulative strategy returns
                    cumulative_return = results['Cumulative_Strategy_Returns'].iloc[-1]

                    # Print current parameters and their cumulative return for debugging
                    print(f"Testing params: short_window={short_window}, long_window={long_window}, "
                          f"stop_loss={stop_loss}, take_profit={take_profit} => "
                          f"Cumulative Return: {cumulative_return:.2%}")

                    # Update best parameters if the current returns are better
                    if cumulative_return > best_return:
                        best_return = cumulative_return
                        best_params = {
                            'short_window': short_window,
                            'long_window': long_window,
                            'stop_loss': stop_loss,
                            'take_profit': take_profit
                        }
                        best_results = results

                        # Print performance metrics for the best parameters
    print("\nPerformance Metrics for Best Parameters:")
    print_performance_metrics(best_results)

    return best_params, best_return

if __name__ == "__main__":
    # Define multiple cryptocurrency tickers
    tickers = ["BTC-USD", "ETH-USD"]  # Bitcoin and Ethereum
    start_date = "2020-01-01"
    end_date = "2024-01-01"
    
    # Fetch data for multiple tickers
    crypto_data_dict = fetch_crypto_data_multiple(tickers, start_date, end_date)
    
    # Display quarterwise data for each ticker
    for ticker, data in crypto_data_dict.items():
        print(f"\n--- {ticker} ---")
        display_quarterwise_data({ticker: data})

        # Perform hyperparameter tuning on the ticker's data
        best_params, best_return = hyperparameter_tuning(data)
        print(f"\nBest parameters for {ticker}: {best_params} with a cumulative return of {best_return:.2%}")
