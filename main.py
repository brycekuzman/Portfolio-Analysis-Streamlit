from analytics.data import get_price_data, get_expense_ratios, get_current_prices
from analytics.performance import calculate_portfolio_returns, performance_stats, calculate_individual_returns
from analytics.reporting import plot_growth

# Example portfolio with dollar amounts
portfolio_dollars = {"AAPL": 10000, "PULS": 10000, "TSLA": 10000}  
start, end = "2015-09-30", "2025-08-29"
advisory_fee = 0.00  # 1%

# Get current prices to calculate weights
current_prices = get_current_prices(list(portfolio_dollars.keys()))

# Calculate weights based on dollar amounts and current prices
total_value = sum(portfolio_dollars.values())
portfolio_weights = {}

for ticker, dollar_amount in portfolio_dollars.items():
    shares = dollar_amount / current_prices[ticker]
    portfolio_weights[ticker] = dollar_amount / total_value

print(f"\nPortfolio allocation based on ${total_value:,.0f} investment:")
for ticker, weight in portfolio_weights.items():
    dollar_amount = portfolio_dollars[ticker]
    shares = dollar_amount / current_prices[ticker]
    print(f"{ticker}: ${dollar_amount:,.0f} ({weight:.1%}) - {shares:.2f} shares at ${current_prices[ticker]:.2f}")

# Load historical data
prices = get_price_data(list(portfolio_dollars.keys()), start, end)
expense_ratios = get_expense_ratios(portfolio_dollars.keys())

# Run analysis
port_returns = calculate_portfolio_returns(prices, portfolio_weights, advisory_fee, expense_ratios)
stats, cumulative = performance_stats(port_returns)
individual_returns = calculate_individual_returns(prices)

# Print individual asset returns
print(f"\nIndividual Asset Total Returns ({prices.index[0].strftime('%Y-%m-%d')} to {prices.index[-1].strftime('%Y-%m-%d')}):")
for ticker, return_pct in individual_returns.items():
    print(f"{ticker}: {return_pct:.2%}")

# Print portfolio results
print("\nPortfolio Performance Stats:")
for k, v in stats.items():
    print(f"{k}: {v:.2%}")

# Plot
plot_growth(cumulative).show()
