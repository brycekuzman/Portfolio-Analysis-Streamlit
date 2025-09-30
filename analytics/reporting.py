import matplotlib.pyplot as plt

def plot_growth(cumulative, title="Growth of $1"):
    plt.figure(figsize=(10,6))
    cumulative.plot()
    plt.title(title)
    plt.ylabel("Portfolio Value ($)")
    plt.grid(True)
    return plt
import matplotlib.pyplot as plt


def plot_growth(cumulative, title="Growth of $1"):
    plt.figure(figsize=(10,6))
    cumulative.plot()
    plt.title(title)
    plt.ylabel("Portfolio Value ($)")
    plt.grid(True)
    return plt


def print_portfolio_summary(portfolio):
    """Print detailed portfolio summary."""
    summary = portfolio.get_portfolio_summary()
    
    print(f"\n{'='*60}")
    print(f"ANALYZING {summary['name'].upper()} PORTFOLIO")
    print(f"{'='*60}")
    
    print(f"\nPortfolio allocation based on ${summary['total_value']:,.0f} investment:")
    for holding in summary['holdings']:
        er_display = f" (ER: {holding['expense_ratio']:.2%})" if holding['expense_ratio'] > 0 else " (ER: 0.00%)"
        print(f"{holding['ticker']}: ${holding['dollar_amount']:,.0f} ({holding['weight']:.1%}) - "
              f"{holding['shares']:.2f} shares at ${holding['price']:.2f}{er_display} [{holding['classification']}]")
    
    print(f"\nWeighted Average Expense Ratio: {summary['weighted_avg_er']:.2%}")
    if summary['advisory_fee'] > 0:
        print(f"Advisory Fee: {summary['advisory_fee']:.2%}")
        print(f"Total Annual Fees: {summary['total_fees']:.2%}")
    
    print(f"\nAsset Class Allocation:")
    for asset_class, allocation in sorted(summary['asset_class_allocation'].items()):
        dollar_amount = allocation * summary['total_value']
        print(f"{asset_class}: ${dollar_amount:,.0f} ({allocation:.1%})")


def print_historical_performance(portfolio, results):
    """Print historical performance results."""
    print(f"\nIndividual Asset Total Returns ({results['actual_start_date']} to {results['actual_end_date']}):")
    for ticker, return_pct in results['individual_returns'].items():
        print(f"{ticker}: {return_pct:.2%}")
    
    print(f"\n{portfolio.name} Portfolio Performance Stats (After All Fees):")
    for k, v in results['stats_with_fees'].items():
        if k == "Sharpe Ratio":
            print(f"{k}: {v:.2f}")
        else:
            print(f"{k}: {v:.2%}")
    
    if portfolio.advisory_fee > 0:
        print(f"\n{portfolio.name} Portfolio Performance Stats (Before Advisory Fee):")
        for k, v in results['stats_no_advisory'].items():
            if k == "Sharpe Ratio":
                print(f"{k}: {v:.2f}")
            else:
                print(f"{k}: {v:.2%}")


def print_projection_comparison(current_portfolio, model_portfolio, current_projections, model_projections, total_investment):
    """Print 10-year projection comparison."""
    print(f"\n{'='*60}")
    print("10-YEAR PORTFOLIO PROJECTIONS")
    print(f"{'='*60}")
    
    # Fee comparison
    current_summary = current_portfolio.get_portfolio_summary()
    model_summary = model_portfolio.get_portfolio_summary()
    
    print(f"\nFee Comparison:")
    print(f"Current Portfolio - Weighted Avg Expense Ratio: {current_summary['weighted_avg_er']:.2%}, "
          f"Advisory Fee: {current_summary['advisory_fee']:.2%}, Total: {current_summary['total_fees']:.2%}")
    print(f"{model_summary['name']} Portfolio - Weighted Avg Expense Ratio: {model_summary['weighted_avg_er']:.2%}, "
          f"Advisory Fee: {model_summary['advisory_fee']:.2%}, Total: {model_summary['total_fees']:.2%}")
    
    fee_difference = model_summary['total_fees'] - current_summary['total_fees']
    print(f"Fee Difference: {fee_difference:+.2%}")
    
    # Asset class allocations
    from .models import growth_rates
    
    print(f"\nCurrent Portfolio Asset Class Allocation:")
    for asset_class, allocation in sorted(current_summary['asset_class_allocation'].items()):
        growth_rate = growth_rates.get(asset_class, 0)
        print(f"  {asset_class}: {allocation:.1%} (Est. Growth: {growth_rate:.1%})")
    
    print(f"\n{model_summary['name']} Portfolio Asset Class Allocation:")
    for asset_class, allocation in sorted(model_summary['asset_class_allocation'].items()):
        growth_rate = growth_rates.get(asset_class, 0)
        print(f"  {asset_class}: {allocation:.1%} (Est. Growth: {growth_rate:.1%})")


def print_fee_breakdown(current_portfolio, model_portfolio, total_investment):
    """Print detailed fee breakdown for 10-year projections."""
    current_projections = current_portfolio.project_future_returns(10)
    model_projections = model_portfolio.project_future_returns(10)
    
    current_summary = current_portfolio.get_portfolio_summary()
    model_summary = model_portfolio.get_portfolio_summary()
    
    # Calculate projections with and without advisory fees
    current_gross_return = current_projections['weighted_annual_return']
    model_gross_return = model_projections['weighted_annual_return']
    
    current_net_return = current_gross_return - current_summary['weighted_avg_er'] - current_summary['advisory_fee']
    model_net_return = model_gross_return - model_summary['weighted_avg_er'] - model_summary['advisory_fee']
    
    current_gross_final = total_investment * ((1 + current_gross_return) ** 10)
    model_gross_final = total_investment * ((1 + model_gross_return) ** 10)
    current_net_final = total_investment * ((1 + current_net_return) ** 10)
    model_net_final = total_investment * ((1 + model_net_return) ** 10)
    
    print(f"\n10-Year Fee Impact Breakdown:")
    print("=" * 60)
    
    # Calculate the dollar impact of each fee component over 10 years
    current_only_expense_return = current_gross_return - current_summary['weighted_avg_er']
    current_only_expense_final = total_investment * ((1 + current_only_expense_return) ** 10)
    
    model_only_expense_return = model_gross_return - model_summary['weighted_avg_er']
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
    print(f"Current Portfolio Advisory Fee Cost: ${current_advisory_cost:,.0f} ({current_summary['advisory_fee']:.2%} annually)")
    print(f"{model_summary['name']} Portfolio Advisory Fee Cost: ${model_advisory_cost:,.0f} ({model_summary['advisory_fee']:.2%} annually)")
    print(f"Advisory Fee Difference: ${advisory_fee_difference:+,.0f}")
    
    print(f"\nExpense Ratio Impact (10-year dollar cost):")
    print(f"Current Portfolio Expense Ratio Cost: ${current_expense_cost:,.0f} ({current_summary['weighted_avg_er']:.2%} annually)")
    print(f"{model_summary['name']} Portfolio Expense Ratio Cost: ${model_expense_cost:,.0f} ({model_summary['weighted_avg_er']:.2%} annually)")
    print(f"Expense Ratio Difference: ${expense_ratio_difference:+,.0f}")
    
    print(f"\nTotal Fee Impact Summary:")
    total_current_fees = current_advisory_cost + current_expense_cost
    total_model_fees = model_advisory_cost + model_expense_cost
    total_fee_difference = total_model_fees - total_current_fees
    
    print(f"Current Portfolio Total Fee Cost: ${total_current_fees:,.0f}")
    print(f"{model_summary['name']} Portfolio Total Fee Cost: ${total_model_fees:,.0f}")
    print(f"Total Fee Difference: ${total_fee_difference:+,.0f}")
    
    if total_fee_difference < 0:
        print(f"💰 The {model_summary['name']} portfolio saves ${abs(total_fee_difference):,.0f} in fees over 10 years!")
    else:
        print(f"⚠️  The {model_summary['name']} portfolio costs ${total_fee_difference:,.0f} more in fees over 10 years.")


def plot_portfolio_comparison(current_results, model_results, model_name):
    """Plot portfolio growth comparison."""
    plt.figure(figsize=(12, 8))
    plt.plot(current_results['cumulative_with_fees'].index, 
             current_results['cumulative_with_fees'].values, 
             label='Current Portfolio (After Fees)', linewidth=2)
    plt.plot(model_results['cumulative_with_fees'].index, 
             model_results['cumulative_with_fees'].values, 
             label=f'{model_name} Model (After Fees)', linewidth=2)
    plt.title('Portfolio Growth Comparison (After All Fees)')
    plt.ylabel('Portfolio Value ($)')
    plt.xlabel('Date')
    plt.legend()
    plt.grid(True)
    plt.show()
