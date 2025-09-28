import numpy as np
import pandas as pd

def calculate_portfolio_returns(prices, weights, advisory_fee=0.0, expense_ratios=None):
    returns = prices.pct_change().dropna()
    weights = np.array(list(weights.values()))
    port_returns = returns.dot(weights)

    # Deduct advisory fee daily
    daily_advisory = (1 - advisory_fee) ** (1/252)
    port_returns = (1 + port_returns) * daily_advisory - 1

    # Deduct expense ratios daily
    if expense_ratios:
        for ticker, weight in weights_dict.items():
            er = expense_ratios.get(ticker, 0.0)
            if er > 0:
                daily_er = (1 - er) ** (1/252)
                port_returns = (1 + port_returns) * (daily_er ** weight) - 1

    return port_returns

def performance_stats(port_returns, risk_free=0.02):
    cumulative = (1 + port_returns).cumprod()
    total_return = cumulative.iloc[-1] - 1
    annualized_return = (1 + total_return) ** (252/len(port_returns)) - 1
    volatility = port_returns.std() * np.sqrt(252)
    sharpe = (annualized_return - risk_free) / volatility
    max_dd = ((cumulative / cumulative.cummax()) - 1).min()

    return {
        "Total Return": total_return,
        "Annualized Return": annualized_return,
        "Volatility": volatility,
        "Sharpe Ratio": sharpe,
        "Max Drawdown": max_dd
    }, cumulative
