# metrics.py
import numpy as np
import pandas as pd

def calculate_max_drawdown(cumulative_returns):
    """
    Calculate the maximum drawdown from cumulative returns.
    
    Parameters:
    cumulative_returns (pd.Series): Series of cumulative returns.

    Returns:
    float: Maximum drawdown value.
    """
    # Calculate the running maximum
    running_max = cumulative_returns.cummax()
    
    # Calculate drawdowns
    drawdowns = (cumulative_returns - running_max) / running_max
    
    # Return the maximum drawdown
    return drawdowns.min()  # Returns the most negative value

def print_performance_metrics(data: pd.DataFrame):
    """
    Prints performance metrics for the trading strategy.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing strategy returns and other metrics.
    """
    # Calculate performance metrics
    cumulative_returns = (1 + data['Strategy_Return']).cumprod() - 1
    
    # Calculate Sharpe Ratio
    sharpe_ratio = (data['Strategy_Return'].mean() / data['Strategy_Return'].std()) * np.sqrt(252)  # Annualized Sharpe Ratio

    # Calculate Maximum Drawdown
    max_drawdown = calculate_max_drawdown(cumulative_returns)

    # Calculate Annualized Return
    annualized_return = cumulative_returns[-1] / (len(data) / 252)  # Assuming 252 trading days

    # Print metrics
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
    print(f"Maximum Drawdown: {max_drawdown:.2%}")
    print(f"Annualized Return: {annualized_return:.2%}")
