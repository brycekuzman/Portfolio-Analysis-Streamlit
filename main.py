
from analytics.data import get_price_data, get_expense_ratios, get_current_prices, get_investment_classifications
from analytics.performance import calculate_portfolio_returns, performance_stats, calculate_individual_returns
from analytics.reporting import plot_growth
from analytics.models import model_portfolios, growth_rates

def get_user_portfolio():
    """Get user's current portfolio input."""
    print("Enter your current portfolio (ticker: dollar_amount):")
    print("Example: AAPL:10000,MSFT:5000")
    print("Or press Enter to use default: AAPL:10000,PULS:10000")
    
    user_input = input("Portfolio: ").strip()
    
    if not user_input:
        return {"AAPL": 10000, "PULS": 10000}
    
    portfolio = {}
    try:
        for item in user_input.split(','):
            ticker, amount = item.strip().split(':')
            portfolio[ticker.upper()] = float(amount)
        return portfolio
    except ValueError:
        print("Invalid format. Using default portfolio.")
        return {"AAPL": 10000, "PULS": 10000}

def get_model_portfolio_choice():
    """Get user's model portfolio selection."""
    print("\nAvailable Model Portfolios:")
    for i, name in enumerate(model_portfolios.keys(), 1):
        print(f"{i}. {name}")
        allocations = model_portfolios[name]
        for ticker, weight in allocations.items():
            print(f"   {ticker}: {weight:.0%}")
        print()
    
    while True:
        try:
            choice = input("Select model portfolio (1-5): ").strip()
            choice_num = int(choice)
            if 1 <= choice_num <= len(model_portfolios):
                portfolio_name = list(model_portfolios.keys())[choice_num - 1]
                return portfolio_name, model_portfolios[portfolio_name]
            else:
                print("Invalid choice. Please enter 1-5.")
        except ValueError:
            print("Invalid input. Please enter a number 1-5.")
        except KeyboardInterrupt:
            print("\nUsing default: Conservative portfolio")
            return "Conservative", model_portfolios["Conservative"]

def analyze_portfolio(portfolio_dollars, portfolio_name, start, end, advisory_fee):
    """Analyze a portfolio and return results."""
    print(f"\n{'='*60}")
    print(f"ANALYZING {portfolio_name.upper()} PORTFOLIO")
    print(f"{'='*60}")
    
    # Get current prices to calculate weights
    current_prices = get_current_prices(list(portfolio_dollars.keys()))
    
    # Calculate weights based on dollar amounts and current prices
    total_value = sum(portfolio_dollars.values())
    portfolio_weights = {}
    
    for ticker, dollar_amount in portfolio_dollars.items():
        shares = dollar_amount / current_prices[ticker]
        portfolio_weights[ticker] = dollar_amount / total_value
    
    # Load expense ratios and classifications
    expense_ratios = get_expense_ratios(portfolio_dollars.keys())
    classifications = get_investment_classifications(portfolio_dollars.keys())
    
    # Calculate weighted average expense ratio
    weighted_avg_er = sum(portfolio_weights[ticker] * expense_ratios[ticker] for ticker in portfolio_weights.keys())
    
    print(f"\nPortfolio allocation based on ${total_value:,.0f} investment:")
    for ticker, weight in portfolio_weights.items():
        dollar_amount = portfolio_dollars[ticker]
        shares = dollar_amount / current_prices[ticker]
        er = expense_ratios[ticker]
        classification = classifications[ticker]
        er_display = f" (ER: {er:.2%})" if er > 0 else " (ER: 0.00%)"
        print(f"{ticker}: ${dollar_amount:,.0f} ({weight:.1%}) - {shares:.2f} shares at ${current_prices[ticker]:.2f}{er_display} [{classification}]")
    
    print(f"\nWeighted Average Expense Ratio: {weighted_avg_er:.2%}")
    
    # Calculate allocation by asset class
    asset_class_allocation = {}
    for ticker, weight in portfolio_weights.items():
        asset_class = classifications[ticker]
        if asset_class in asset_class_allocation:
            asset_class_allocation[asset_class] += weight
        else:
            asset_class_allocation[asset_class] = weight
    
    print(f"\nAsset Class Allocation:")
    for asset_class, allocation in sorted(asset_class_allocation.items()):
        dollar_amount = allocation * total_value
        print(f"{asset_class}: ${dollar_amount:,.0f} ({allocation:.1%})")
    
    # Load historical data
    prices = get_price_data(list(portfolio_dollars.keys()), start, end)
    
    # Run analysis
    port_returns = calculate_portfolio_returns(prices, portfolio_weights, advisory_fee, expense_ratios)
    stats, cumulative = performance_stats(port_returns)
    individual_returns = calculate_individual_returns(prices)
    
    # Print individual asset returns
    print(f"\nIndividual Asset Total Returns ({prices.index[0].strftime('%Y-%m-%d')} to {prices.index[-1].strftime('%Y-%m-%d')}):")
    for ticker, return_pct in individual_returns.items():
        print(f"{ticker}: {return_pct:.2%}")
    
    # Print portfolio results
    print(f"\n{portfolio_name} Portfolio Performance Stats:")
    for k, v in stats.items():
        if k == "Sharpe Ratio":
            print(f"{k}: {v:.2f}")
        else:
            print(f"{k}: {v:.2%}")
    
    return stats, cumulative, portfolio_weights, asset_class_allocation

def main():
    # Get user inputs
    portfolio_dollars = get_user_portfolio()
    model_name, model_allocations = get_model_portfolio_choice()
    
    start, end = "2015-09-30", "2025-08-29"
    advisory_fee = 0.00  # 0%
    
    # Analyze current portfolio
    current_stats, current_cumulative, current_weights, current_asset_allocation = analyze_portfolio(
        portfolio_dollars, "CURRENT", start, end, advisory_fee
    )
    
    # Convert model portfolio allocations to dollar amounts
    total_investment = sum(portfolio_dollars.values())
    model_portfolio_dollars = {}
    for ticker, weight in model_allocations.items():
        model_portfolio_dollars[ticker] = total_investment * weight
    
    # Analyze model portfolio
    model_stats, model_cumulative, model_weights, model_asset_allocation = analyze_portfolio(
        model_portfolio_dollars, model_name.upper(), start, end, advisory_fee
    )
    
    # Future projections
    from analytics.models import growth_rates
    from analytics.performance import project_portfolio_returns
    
    print(f"\n{'='*60}")
    print("10-YEAR PORTFOLIO PROJECTIONS")
    print(f"{'='*60}")
    
    # Project current portfolio
    current_projections = project_portfolio_returns(current_asset_allocation, growth_rates, years=10)
    model_projections = project_portfolio_returns(model_asset_allocation, growth_rates, years=10)
    
    print(f"\nCurrent Portfolio Asset Class Allocation:")
    for asset_class, allocation in sorted(current_asset_allocation.items()):
        growth_rate = growth_rates.get(asset_class, 0)
        print(f"  {asset_class}: {allocation:.1%} (Est. Growth: {growth_rate:.1%})")
    
    print(f"\n{model_name} Portfolio Asset Class Allocation:")
    for asset_class, allocation in sorted(model_asset_allocation.items()):
        growth_rate = growth_rates.get(asset_class, 0)
        print(f"  {asset_class}: {allocation:.1%} (Est. Growth: {growth_rate:.1%})")
    
    print(f"\n10-Year Projection Results:")
    total_investment = sum(portfolio_dollars.values())
    
    current_weighted_return = current_projections['weighted_annual_return']
    model_weighted_return = model_projections['weighted_annual_return']
    
    current_final_value = total_investment * current_projections['final_portfolio_value']
    model_final_value = total_investment * model_projections['final_portfolio_value']
    
    print(f"{'Portfolio':<25} {'Est. Annual Return':<18} {'Final Value':<15} {'Total Return':<15}")
    print("-" * 75)
    print(f"{'Current':<25} {current_weighted_return:<18.2%} ${current_final_value:<14,.0f} {current_projections['total_projected_return']:<15.2%}")
    print(f"{model_name:<25} {model_weighted_return:<18.2%} ${model_final_value:<14,.0f} {model_projections['total_projected_return']:<15.2%}")
    
    value_difference = model_final_value - current_final_value
    return_difference = model_projections['total_projected_return'] - current_projections['total_projected_return']
    print(f"{'Difference':<25} {model_weighted_return - current_weighted_return:<18.2%} ${value_difference:<14,.0f} {return_difference:<15.2%}")
    
    # Comparison summary
    print(f"\n{'='*60}")
    print("HISTORICAL PORTFOLIO COMPARISON SUMMARY")
    print(f"{'='*60}")
    
    print(f"\n{'Metric':<20} {'Current':<15} {model_name:<15} {'Difference':<15}")
    print("-" * 65)
    
    for metric in ["Total Return", "Annualized Return", "Volatility", "Max Drawdown"]:
        current_val = current_stats[metric]
        model_val = model_stats[metric]
        diff = model_val - current_val
        
        if metric == "Sharpe Ratio":
            print(f"{metric:<20} {current_val:<15.2f} {model_val:<15.2f} {diff:<15.2f}")
        else:
            print(f"{metric:<20} {current_val:<15.2%} {model_val:<15.2%} {diff:<15.2%}")
    
    # Sharpe ratio comparison
    current_sharpe = current_stats["Sharpe Ratio"]
    model_sharpe = model_stats["Sharpe Ratio"]
    sharpe_diff = model_sharpe - current_sharpe
    print(f"{'Sharpe Ratio':<20} {current_sharpe:<15.2f} {model_sharpe:<15.2f} {sharpe_diff:<15.2f}")
    
    # Plot both portfolios
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 8))
    plt.plot(current_cumulative.index, current_cumulative.values, label='Current Portfolio', linewidth=2)
    plt.plot(model_cumulative.index, model_cumulative.values, label=f'{model_name} Model', linewidth=2)
    plt.title('Portfolio Growth Comparison')
    plt.ylabel('Portfolio Value ($)')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
