import numpy as np
import pandas as pd

def calculate_portfolio_returns(prices, weights, advisory_fee=0.0, expense_ratios=None):
    returns = prices.pct_change().dropna()
    weights_array = np.array(list(weights.values()))
    port_returns = returns.dot(weights_array)

    # Deduct advisory fee daily
    daily_advisory = (1 - advisory_fee) ** (1/252)
    port_returns = (1 + port_returns) * daily_advisory - 1

    # Deduct expense ratios daily
    if expense_ratios:
        for ticker, weight in weights.items():
            er = expense_ratios.get(ticker, 0.0)
            if er > 0:
                daily_er = (1 - er) ** (1/252)
                port_returns = (1 + port_returns) * (daily_er ** weight) - 1

    return port_returns

def calculate_individual_returns(prices):
    """Calculate total return for each individual asset."""
    individual_returns = {}
    
    for ticker in prices.columns:
        start_price = prices[ticker].iloc[0]
        end_price = prices[ticker].iloc[-1]
        total_return = (end_price - start_price) / start_price
        individual_returns[ticker] = total_return
    
    return individual_returns


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



def project_portfolio_returns(asset_class_allocation, growth_rates, years=10):
    """
    Project portfolio returns based on asset class allocations and growth rates.
    
    Args:
        asset_class_allocation: Dict of asset class -> weight
        growth_rates: Dict of asset class -> annual growth rate
        years: Number of years to project
    
    Returns:
        Dict with projection results
    """
    # Calculate weighted average annual return
    weighted_annual_return = sum(
        asset_class_allocation.get(asset_class, 0) * growth_rate
        for asset_class, growth_rate in growth_rates.items()
    )
    
    # Calculate total return over the projection period
    total_projected_return = (1 + weighted_annual_return) ** years - 1
    
    # Calculate year-by-year projections
    yearly_projections = []
    portfolio_value = 1.0  # Start with $1
    
    for year in range(1, years + 1):
        portfolio_value *= (1 + weighted_annual_return)
        yearly_projections.append({
            'year': year,
            'portfolio_value': portfolio_value,
            'annual_return': weighted_annual_return,
            'cumulative_return': portfolio_value - 1
        })
    
    return {
        'weighted_annual_return': weighted_annual_return,
        'total_projected_return': total_projected_return,
        'final_portfolio_value': portfolio_value,
        'yearly_projections': yearly_projections
    }
