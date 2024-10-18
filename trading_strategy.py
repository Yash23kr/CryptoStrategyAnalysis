# trading_strategy.py
import pandas as pd
import numpy as np
from sklearn.model_selection import ParameterGrid

def apply_moving_average_strategy(crypto_data: pd.DataFrame, short_window: int = 20, long_window: int = 50) -> pd.DataFrame:
    """
    Applies a simple moving average crossover strategy.

    Parameters:
    crypto_data (pd.DataFrame): Historical price data for the cryptocurrency.
    short_window (int): Short moving average window.
    long_window (int): Long moving average window.

    Returns:
    pd.DataFrame: DataFrame containing original data and signals.
    """
    # Calculate moving averages
    crypto_data['SMA_Short'] = crypto_data['Close'].rolling(window=short_window).mean()
    crypto_data['SMA_Long'] = crypto_data['Close'].rolling(window=long_window).mean()

    # Generate signals
    crypto_data['Signal'] = 0
    crypto_data['Signal'][short_window:] = np.where(
        crypto_data['SMA_Short'][short_window:] > crypto_data['SMA_Long'][short_window:], 1, 0
    )
    crypto_data['Position'] = crypto_data['Signal'].diff().fillna(0)  # Fill NA values to avoid KeyErrors

    return crypto_data

def apply_risk_management(crypto_data: pd.DataFrame, stop_loss: float = 0.05, take_profit: float = 0.10) -> pd.DataFrame:
    """
    Applies stop-loss and take-profit logic to the strategy.

    Parameters:
    crypto_data (pd.DataFrame): DataFrame containing price data and signals.
    stop_loss (float): The percentage loss at which to exit a trade.
    take_profit (float): The percentage gain at which to exit a trade.

    Returns:
    pd.DataFrame: DataFrame with managed positions.
    """
    # Initialize managed position column
    crypto_data['Managed_Position'] = 0

    for i in range(1, len(crypto_data)):
        # Check if we have a buy signal
        if crypto_data['Signal'].iloc[i] == 1:  # Buy signal
            crypto_data['Managed_Position'].iloc[i] = 1
        elif crypto_data['Signal'].iloc[i] == 0:  # Sell signal
            crypto_data['Managed_Position'].iloc[i] = 0

        # Implement stop-loss and take-profit logic
        if crypto_data['Managed_Position'].iloc[i - 1] == 1:  # Currently in position
            # Check if stop-loss condition is met
            if (crypto_data['Close'].iloc[i] < crypto_data['Close'].iloc[i - 1] * (1 - stop_loss)):
                crypto_data['Managed_Position'].iloc[i] = 0  # Exit position
            # Check if take-profit condition is met
            elif (crypto_data['Close'].iloc[i] > crypto_data['Close'].iloc[i - 1] * (1 + take_profit)):
                crypto_data['Managed_Position'].iloc[i] = 0  # Exit position

    return crypto_data

def backtest_strategy(crypto_data: pd.DataFrame) -> pd.DataFrame:
    """
    Backtests the trading strategy.

    Parameters:
    crypto_data (pd.DataFrame): DataFrame containing price data and signals.

    Returns:
    pd.DataFrame: DataFrame with strategy returns and cumulative returns.
    """
    # Calculate daily returns
    crypto_data['Daily_Return'] = crypto_data['Close'].pct_change()

    # Calculate strategy returns based on managed positions
    crypto_data['Strategy_Return'] = crypto_data['Daily_Return'] * crypto_data['Managed_Position'].shift(1)

    # Calculate cumulative returns
    crypto_data['Cumulative_Market_Returns'] = (1 + crypto_data['Daily_Return']).cumprod() - 1
    crypto_data['Cumulative_Strategy_Returns'] = (1 + crypto_data['Strategy_Return']).cumprod() - 1

    return crypto_data

def tune_hyperparameters(crypto_data: pd.DataFrame, short_windows: list, long_windows: list, stop_losses: list, take_profits: list) -> dict:
    """
    Tunes hyperparameters for the moving average strategy and returns the best parameters based on cumulative returns.

    Parameters:
    crypto_data (pd.DataFrame): DataFrame containing price data.
    short_windows (list): List of short window values to test.
    long_windows (list): List of long window values to test.
    stop_losses (list): List of stop-loss percentages to test.
    take_profits (list): List of take-profit percentages to test.

    Returns:
    dict: Best parameters based on cumulative strategy returns.
    """
    best_params = None
    best_return = -np.inf

    param_grid = ParameterGrid({
        'short_window': short_windows,
        'long_window': long_windows,
        'stop_loss': stop_losses,
        'take_profit': take_profits
    })

    for params in param_grid:
    # Apply the moving average strategy
        strategy_data = apply_moving_average_strategy(crypto_data, params['short_window'], params['long_window'])
        # Apply risk management
        strategy_data = apply_risk_management(strategy_data, params['stop_loss'], params['take_profit'])
        # Backtest the strategy
        results = backtest_strategy(strategy_data)

        # Check cumulative strategy returns
        cumulative_return = results['Cumulative_Strategy_Returns'].iloc[-1]

        # Print current parameters and their cumulative return for debugging
        print(f"Testing params: {params} => Cumulative Return: {cumulative_return}")

        # Update best parameters if the current returns are better
        if cumulative_return > best_return:
            best_return = cumulative_return
            best_params = params


    return best_params

if __name__ == "__main__":
    # Example usage (this would be moved to the main file)
    pass
