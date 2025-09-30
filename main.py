from analytics.portfolio import Portfolio
from analytics.reporting import (
    print_portfolio_summary, print_historical_performance,
    print_projection_comparison, print_fee_breakdown, plot_portfolio_comparison
)
from analytics.user_input import get_user_portfolio, get_model_portfolio_choice
from analytics.models import model_fee
import matplotlib.pyplot as plt


def main():
    # Get user inputs
    portfolio_dollars = get_user_portfolio()
    
    start, end = "2015-09-30", "2025-08-29"
    current_advisory_fee = 0.01  # 1%

    # Create portfolio objects
    current_portfolio = Portfolio(portfolio_dollars, "CURRENT", current_advisory_fee)

    # Get the best matching model portfolio based on current asset allocation
    model_name, model_allocations = get_model_portfolio_choice(current_portfolio.asset_class_allocation)

    # Analyze current portfolio first to get actual start date
    print_portfolio_summary(current_portfolio)
    current_results = current_portfolio.analyze_historical_performance(start, end)
    print_historical_performance(current_portfolio, current_results)

    # Use the actual start date from current portfolio for model portfolio analysis
    actual_start_date = current_results['actual_start_date']

    # Convert model portfolio allocations to dollar amounts
    total_investment = sum(portfolio_dollars.values())
    model_portfolio_dollars = {}
    for ticker, weight in model_allocations.items():
        model_portfolio_dollars[ticker] = total_investment * weight

    # Create and analyze model portfolio using the same start date
    model_portfolio = Portfolio(model_portfolio_dollars, model_name.upper(), model_fee)
    print_portfolio_summary(model_portfolio)
    model_results = model_portfolio.analyze_historical_performance(actual_start_date, end)
    print_historical_performance(model_portfolio, model_results)

    # Future projections
    current_projections = current_portfolio.project_future_returns(10)
    model_projections = model_portfolio.project_future_returns(10)

    print_projection_comparison(current_portfolio, model_portfolio, current_projections, model_projections, total_investment)
    print_fee_breakdown(current_portfolio, model_portfolio, total_investment)

    # Historical comparison summary
    print_historical_comparison_summary(current_portfolio, model_portfolio, current_results, model_results)

    # Plot comparison
    plot_portfolio_comparison(current_results, model_results, model_name)


def print_historical_comparison_summary(current_portfolio, model_portfolio, current_results, model_results):
    """Print historical portfolio comparison summary."""
    current_summary = current_portfolio.get_portfolio_summary()
    model_summary = model_portfolio.get_portfolio_summary()

    print(f"\n{'='*60}")
    print("HISTORICAL PORTFOLIO COMPARISON SUMMARY")
    print(f"{'='*60}")
    print(f"Analysis Period: {current_results['actual_start_date']} to {current_results['actual_end_date']}")

    print(f"\nFee Impact on Historical Returns:")
    print(f"Current Portfolio:")
    print(f"  After All Fees: {current_results['stats_with_fees']['Annualized Return']:.2%}")
    if current_summary['advisory_fee'] > 0:
        print(f"  Before Advisory Fee: {current_results['stats_no_advisory']['Annualized Return']:.2%}")
        advisory_impact = current_results['stats_no_advisory']['Annualized Return'] - current_results['stats_with_fees']['Annualized Return']
        print(f"  Advisory Fee Impact: -{advisory_impact:.2%}")

    print(f"\n{model_summary['name']} Portfolio:")
    print(f"  After All Fees: {model_results['stats_with_fees']['Annualized Return']:.2%}")
    print(f"  Before Advisory Fee: {model_results['stats_no_advisory']['Annualized Return']:.2%}")
    model_advisory_impact = model_results['stats_no_advisory']['Annualized Return'] - model_results['stats_with_fees']['Annualized Return']
    print(f"  Advisory Fee Impact: -{model_advisory_impact:.2%}")

    print(f"\n{'Metric':<20} {'Current':<15} {model_summary['name']:<15} {'Difference':<15}")
    print("-" * 65)

    for metric in ["Total Return", "Annualized Return", "Volatility", "Max Drawdown"]:
        current_val = current_results['stats_with_fees'][metric]
        model_val = model_results['stats_with_fees'][metric]
        diff = model_val - current_val

        print(f"{metric:<20} {current_val:<15.2%} {model_val:<15.2%} {diff:<15.2%}")

    # Sharpe ratio comparison
    current_sharpe = current_results['stats_with_fees']["Sharpe Ratio"]
    model_sharpe = model_results['stats_with_fees']["Sharpe Ratio"]
    sharpe_diff = model_sharpe - current_sharpe
    print(f"{'Sharpe Ratio':<20} {current_sharpe:<15.2f} {model_sharpe:<15.2f} {sharpe_diff:<15.2f}")


if __name__ == "__main__":
    main()