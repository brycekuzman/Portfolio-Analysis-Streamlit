from Analytics.data import get_price_data, get_expense_ratios
from Analytics.performance import calculate_portfolio_returns, performance_stats
from Analytics.reporting import plot_growth

# Example portfolio
portfolio = {"AAPL": 0.4, "MSFT": 0.3, "SPY": 0.3}
start, end = "2013-01-01", "2023-01-01"
advisory_fee = 0.01  # 1%

# Load data
prices = get_price_data(list(portfolio.keys()), start, end)
expense_ratios = get_expense_ratios(portfolio.keys())

# Run analysis
port_returns = calculate_portfolio_returns(prices, portfolio, advisory_fee, expense_ratios)
stats, cumulative = performance_stats(port_returns)

# Print results
print("\nPerformance Stats:")
for k, v in stats.items():
    print(f"{k}: {v:.2%}")

# Plot
plot_growth(cumulative).show()
