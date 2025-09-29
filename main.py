
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
    if advisory_fee > 0:
        print(f"Advisory Fee: {advisory_fee:.2%}")
        print(f"Total Annual Fees: {weighted_avg_er + advisory_fee:.2%}")
    
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
    
    # Run analysis with and without advisory fees
    port_returns_with_fees = calculate_portfolio_returns(prices, portfolio_weights, advisory_fee, expense_ratios)
    port_returns_no_advisory = calculate_portfolio_returns(prices, portfolio_weights, 0.0, expense_ratios)
    
    stats_with_fees, cumulative_with_fees = performance_stats(port_returns_with_fees)
    stats_no_advisory, cumulative_no_advisory = performance_stats(port_returns_no_advisory)
    
    individual_returns = calculate_individual_returns(prices)
    
    # Print individual asset returns
    print(f"\nIndividual Asset Total Returns ({prices.index[0].strftime('%Y-%m-%d')} to {prices.index[-1].strftime('%Y-%m-%d')}):")
    for ticker, return_pct in individual_returns.items():
        print(f"{ticker}: {return_pct:.2%}")
    
    # Print portfolio results
    print(f"\n{portfolio_name} Portfolio Performance Stats (After All Fees):")
    for k, v in stats_with_fees.items():
        if k == "Sharpe Ratio":
            print(f"{k}: {v:.2f}")
        else:
            print(f"{k}: {v:.2%}")
    
    if advisory_fee > 0:
        print(f"\n{portfolio_name} Portfolio Performance Stats (Before Advisory Fee):")
        for k, v in stats_no_advisory.items():
            if k == "Sharpe Ratio":
                print(f"{k}: {v:.2f}")
            else:
                print(f"{k}: {v:.2%}")
    
    return {
        'stats_with_fees': stats_with_fees,
        'stats_no_advisory': stats_no_advisory,
        'cumulative_with_fees': cumulative_with_fees,
        'cumulative_no_advisory': cumulative_no_advisory,
        'portfolio_weights': portfolio_weights,
        'asset_class_allocation': asset_class_allocation,
        'weighted_avg_er': weighted_avg_er,
        'actual_start_date': prices.index[0].strftime('%Y-%m-%d'),
        'actual_end_date': prices.index[-1].strftime('%Y-%m-%d')
    }

def main():
    # Get user inputs
    portfolio_dollars = get_user_portfolio()
    model_name, model_allocations = get_model_portfolio_choice()
    
    start, end = "2015-09-30", "2025-08-29"
    current_advisory_fee = 0.01  # 0%
    
    # Analyze current portfolio first to get actual start date
    current_results = analyze_portfolio(
        portfolio_dollars, "CURRENT", start, end, current_advisory_fee
    )
    
    # Use the actual start date from current portfolio for model portfolio analysis
    actual_start_date = current_results['actual_start_date']
    
    # Convert model portfolio allocations to dollar amounts
    total_investment = sum(portfolio_dollars.values())
    model_portfolio_dollars = {}
    for ticker, weight in model_allocations.items():
        model_portfolio_dollars[ticker] = total_investment * weight
    
    # Import model advisory fee
    from analytics.models import model_fee
    
    # Analyze model portfolio using the same start date
    model_results = analyze_portfolio(
        model_portfolio_dollars, model_name.upper(), actual_start_date, end, model_fee
    )
    
    # Future projections
    from analytics.models import growth_rates
    from analytics.performance import project_portfolio_returns
    
    print(f"\n{'='*60}")
    print("10-YEAR PORTFOLIO PROJECTIONS")
    print(f"{'='*60}")
    
    # Project current portfolio
    current_projections = project_portfolio_returns(current_results['asset_class_allocation'], growth_rates, years=10)
    model_projections = project_portfolio_returns(model_results['asset_class_allocation'], growth_rates, years=10)
    
    print(f"\nFee Comparison:")
    print(f"Current Portfolio - Weighted Avg Expense Ratio: {current_results['weighted_avg_er']:.2%}, Advisory Fee: {current_advisory_fee:.2%}, Total: {current_results['weighted_avg_er'] + current_advisory_fee:.2%}")
    print(f"{model_name} Portfolio - Weighted Avg Expense Ratio: {model_results['weighted_avg_er']:.2%}, Advisory Fee: {model_fee:.2%}, Total: {model_results['weighted_avg_er'] + model_fee:.2%}")
    fee_difference = (model_results['weighted_avg_er'] + model_fee) - (current_results['weighted_avg_er'] + current_advisory_fee)
    print(f"Fee Difference: {fee_difference:+.2%}")
    
    print(f"\nCurrent Portfolio Asset Class Allocation:")
    for asset_class, allocation in sorted(current_results['asset_class_allocation'].items()):
        growth_rate = growth_rates.get(asset_class, 0)
        print(f"  {asset_class}: {allocation:.1%} (Est. Growth: {growth_rate:.1%})")
    
    print(f"\n{model_name} Portfolio Asset Class Allocation:")
    for asset_class, allocation in sorted(model_results['asset_class_allocation'].items()):
        growth_rate = growth_rates.get(asset_class, 0)
        print(f"  {asset_class}: {allocation:.1%} (Est. Growth: {growth_rate:.1%})")
    
    # Calculate projections with and without advisory fees
    current_gross_return = current_projections['weighted_annual_return']
    model_gross_return = model_projections['weighted_annual_return']
    
    current_net_return = current_gross_return - current_results['weighted_avg_er'] - current_advisory_fee
    model_net_return = model_gross_return - model_results['weighted_avg_er'] - model_fee
    
    print(f"\n10-Year Projection Results (Before Advisory Fees):")
    total_investment = sum(portfolio_dollars.values())
    
    current_gross_final = total_investment * ((1 + current_gross_return) ** 10)
    model_gross_final = total_investment * ((1 + model_gross_return) ** 10)
    
    print(f"{'Portfolio':<25} {'Est. Annual Return':<18} {'Final Value':<15} {'Total Return':<15}")
    print("-" * 75)
    print(f"{'Current (Gross)':<25} {current_gross_return:<18.2%} ${current_gross_final:<14,.0f} {((current_gross_final/total_investment) - 1):<15.2%}")
    print(f"{model_name + ' (Gross)':<25} {model_gross_return:<18.2%} ${model_gross_final:<14,.0f} {((model_gross_final/total_investment) - 1):<15.2%}")
    
    print(f"\n10-Year Projection Results (After All Fees):")
    current_net_final = total_investment * ((1 + current_net_return) ** 10)
    model_net_final = total_investment * ((1 + model_net_return) ** 10)
    
    print(f"{'Portfolio':<25} {'Est. Annual Return':<18} {'Final Value':<15} {'Total Return':<15}")
    print("-" * 75)
    print(f"{'Current (Net)':<25} {current_net_return:<18.2%} ${current_net_final:<14,.0f} {((current_net_final/total_investment) - 1):<15.2%}")
    print(f"{model_name + ' (Net)':<25} {model_net_return:<18.2%} ${model_net_final:<14,.0f} {((model_net_final/total_investment) - 1):<15.2%}")
    
    value_difference_net = model_net_final - current_net_final
    return_difference_net = model_net_return - current_net_return
    print(f"{'Difference (Net)':<25} {return_difference_net:<18.2%} ${value_difference_net:<14,.0f} {((model_net_final/current_net_final) - 1):<15.2%}")
    
    print(f"\n10-Year Fee Impact Breakdown:")
    print("=" * 60)
    
    # Calculate the dollar impact of each fee component over 10 years
    current_only_expense_return = current_gross_return - current_results['weighted_avg_er']
    current_only_expense_final = total_investment * ((1 + current_only_expense_return) ** 10)
    
    model_only_expense_return = model_gross_return - model_results['weighted_avg_er']
    model_only_expense_final = total_investment * ((1 + model_only_expense_return) ** 10)
    
    # Advisory fee impact
    current_advisory_cost = current_gross_final - current_net_final
    model_advisory_cost = model_gross_final - model_net_final
    advisory_fee_difference = model_advisory_cost - current_advisory_cost
    
    # Expense ratio impact
    current_expense_cost = current_gross_final - current_only_expense_final
    model_expense_cost = model_gross_final - model_only_expense_final
    expense_ratio_difference = model_expense_cost - current_expense_cost
    
    print(f"\nAdvisory Fee Impact (10-year dollar cost):")
    print(f"Current Portfolio Advisory Fee Cost: ${current_advisory_cost:,.0f} ({current_advisory_fee:.2%} annually)")
    print(f"{model_name} Portfolio Advisory Fee Cost: ${model_advisory_cost:,.0f} ({model_fee:.2%} annually)")
    print(f"Advisory Fee Difference: ${advisory_fee_difference:+,.0f}")
    
    print(f"\nExpense Ratio Impact (10-year dollar cost):")
    print(f"Current Portfolio Expense Ratio Cost: ${current_expense_cost:,.0f} ({current_results['weighted_avg_er']:.2%} annually)")
    print(f"{model_name} Portfolio Expense Ratio Cost: ${model_expense_cost:,.0f} ({model_results['weighted_avg_er']:.2%} annually)")
    print(f"Expense Ratio Difference: ${expense_ratio_difference:+,.0f}")
    
    print(f"\nTotal Fee Impact Summary:")
    total_current_fees = current_advisory_cost + current_expense_cost
    total_model_fees = model_advisory_cost + model_expense_cost
    total_fee_difference = total_model_fees - total_current_fees
    
    print(f"Current Portfolio Total Fee Cost: ${total_current_fees:,.0f}")
    print(f"{model_name} Portfolio Total Fee Cost: ${total_model_fees:,.0f}")
    print(f"Total Fee Difference: ${total_fee_difference:+,.0f}")
    
    if total_fee_difference < 0:
        print(f"💰 The {model_name} portfolio saves ${abs(total_fee_difference):,.0f} in fees over 10 years!")
    else:
        print(f"⚠️  The {model_name} portfolio costs ${total_fee_difference:,.0f} more in fees over 10 years.")
    
    # Comparison summary
    print(f"\n{'='*60}")
    print("HISTORICAL PORTFOLIO COMPARISON SUMMARY")
    print(f"{'='*60}")
    print(f"Analysis Period: {current_results['actual_start_date']} to {current_results['actual_end_date']}")
    
    print(f"\nFee Impact on Historical Returns:")
    print(f"Current Portfolio:")
    print(f"  After All Fees: {current_results['stats_with_fees']['Annualized Return']:.2%}")
    if current_advisory_fee > 0:
        print(f"  Before Advisory Fee: {current_results['stats_no_advisory']['Annualized Return']:.2%}")
        advisory_impact = current_results['stats_no_advisory']['Annualized Return'] - current_results['stats_with_fees']['Annualized Return']
        print(f"  Advisory Fee Impact: -{advisory_impact:.2%}")
    
    print(f"\n{model_name} Portfolio:")
    print(f"  After All Fees: {model_results['stats_with_fees']['Annualized Return']:.2%}")
    print(f"  Before Advisory Fee: {model_results['stats_no_advisory']['Annualized Return']:.2%}")
    model_advisory_impact = model_results['stats_no_advisory']['Annualized Return'] - model_results['stats_with_fees']['Annualized Return']
    print(f"  Advisory Fee Impact: -{model_advisory_impact:.2%}")
    
    print(f"\n{'Metric':<20} {'Current':<15} {model_name:<15} {'Difference':<15}")
    print("-" * 65)
    
    for metric in ["Total Return", "Annualized Return", "Volatility", "Max Drawdown"]:
        current_val = current_results['stats_with_fees'][metric]
        model_val = model_results['stats_with_fees'][metric]
        diff = model_val - current_val
        
        if metric == "Sharpe Ratio":
            print(f"{metric:<20} {current_val:<15.2f} {model_val:<15.2f} {diff:<15.2f}")
        else:
            print(f"{metric:<20} {current_val:<15.2%} {model_val:<15.2%} {diff:<15.2%}")
    
    # Sharpe ratio comparison
    current_sharpe = current_results['stats_with_fees']["Sharpe Ratio"]
    model_sharpe = model_results['stats_with_fees']["Sharpe Ratio"]
    sharpe_diff = model_sharpe - current_sharpe
    print(f"{'Sharpe Ratio':<20} {current_sharpe:<15.2f} {model_sharpe:<15.2f} {sharpe_diff:<15.2f}")
    
    # Plot both portfolios
    import matplotlib.pyplot as plt
    plt.figure(figsize=(12, 8))
    plt.plot(current_results['cumulative_with_fees'].index, current_results['cumulative_with_fees'].values, label='Current Portfolio (After Fees)', linewidth=2)
    plt.plot(model_results['cumulative_with_fees'].index, model_results['cumulative_with_fees'].values, label=f'{model_name} Model (After Fees)', linewidth=2)
    plt.title('Portfolio Growth Comparison (After All Fees)')
    plt.ylabel('Portfolio Value ($)')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
