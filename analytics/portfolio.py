
import numpy as np
from .data import get_current_prices, get_expense_ratios, get_investment_classifications, get_price_data
from .performance import calculate_portfolio_returns, performance_stats, calculate_individual_returns, project_portfolio_returns, project_portfolio_with_fees
from .models import growth_rates, asset_volatility


class Portfolio:
    def __init__(self, portfolio_dollars, name, advisory_fee=0.0, asset_class_overrides=None):
        self.portfolio_dollars = portfolio_dollars
        self.name = name
        self.advisory_fee = advisory_fee
        self.total_value = sum(portfolio_dollars.values())
        
        # Calculate weights and get data
        self.current_prices = get_current_prices(list(portfolio_dollars.keys()))
        self.portfolio_weights = self._calculate_weights()
        self.expense_ratios = get_expense_ratios(portfolio_dollars.keys())
        self.classifications = get_investment_classifications(portfolio_dollars.keys(), asset_class_overrides)
        self.weighted_avg_er = self._calculate_weighted_avg_er()
        self.asset_class_allocation = self._calculate_asset_class_allocation()
    
    def _calculate_weights(self):
        """Calculate portfolio weights based on dollar amounts."""
        weights = {}
        for ticker, dollar_amount in self.portfolio_dollars.items():
            weights[ticker] = dollar_amount / self.total_value
        return weights
    
    def _calculate_weighted_avg_er(self):
        """Calculate weighted average expense ratio."""
        return sum(self.portfolio_weights[ticker] * self.expense_ratios[ticker] 
                  for ticker in self.portfolio_weights.keys())
    
    def _calculate_asset_class_allocation(self):
        """Calculate allocation by asset class."""
        allocation = {}
        for ticker, weight in self.portfolio_weights.items():
            asset_class = self.classifications[ticker]
            allocation[asset_class] = allocation.get(asset_class, 0) + weight
        return allocation
    
    def analyze_historical_performance(self, start_date, end_date):
        """Analyze historical portfolio performance."""
        # Load historical data
        prices = get_price_data(list(self.portfolio_dollars.keys()), start_date, end_date)
        
        # Calculate returns with and without advisory fees
        returns_with_fees = calculate_portfolio_returns(
            prices, self.portfolio_weights, self.advisory_fee, self.expense_ratios
        )
        returns_no_advisory = calculate_portfolio_returns(
            prices, self.portfolio_weights, 0.0, self.expense_ratios
        )
        
        # Get performance statistics
        stats_with_fees, cumulative_with_fees = performance_stats(returns_with_fees)
        stats_no_advisory, cumulative_no_advisory = performance_stats(returns_no_advisory)
        
        # Individual asset returns
        individual_returns = calculate_individual_returns(prices)
        
        return {
            'stats_with_fees': stats_with_fees,
            'stats_no_advisory': stats_no_advisory,
            'cumulative_with_fees': cumulative_with_fees,
            'cumulative_no_advisory': cumulative_no_advisory,
            'individual_returns': individual_returns,
            'actual_start_date': prices.index[0].strftime('%Y-%m-%d'),
            'actual_end_date': prices.index[-1].strftime('%Y-%m-%d')
        }
    
    def project_future_returns(self, years=10):
        """Project future portfolio returns."""
        return project_portfolio_returns(self.asset_class_allocation, growth_rates, years)
    
    def project_future_with_fees(self, years=10):
        """Project future portfolio returns with detailed fee calculations."""
        total_fee_rate = self.weighted_avg_er + self.advisory_fee
        return project_portfolio_with_fees(self.asset_class_allocation, growth_rates, total_fee_rate, years)
    
    def calculate_forward_metrics(self, risk_free_rate=0.02):
        """Calculate estimated forward volatility and Sharpe ratio."""
        # Calculate weighted expected return
        expected_return = sum(
            self.asset_class_allocation.get(asset_class, 0) * growth_rate
            for asset_class, growth_rate in growth_rates.items()
        )
        
        # Calculate portfolio volatility using asset class volatilities
        portfolio_variance = 0
        for asset_class, weight in self.asset_class_allocation.items():
            volatility = asset_volatility.get(asset_class, 0)
            portfolio_variance += (weight ** 2) * (volatility ** 2)
        
        # For simplicity, we're not considering correlations between asset classes
        # In practice, you'd want to include a correlation matrix
        portfolio_volatility = portfolio_variance ** 0.5
        
        # Calculate Sharpe ratio
        excess_return = expected_return - risk_free_rate
        sharpe_ratio = excess_return / portfolio_volatility if portfolio_volatility > 0 else 0
        
        return {
            'expected_return': expected_return,
            'portfolio_volatility': portfolio_volatility,
            'sharpe_ratio': sharpe_ratio
        }
    
    def get_portfolio_summary(self):
        """Get a summary of portfolio composition."""
        summary = {
            'name': self.name,
            'total_value': self.total_value,
            'portfolio_weights': self.portfolio_weights,
            'asset_class_allocation': self.asset_class_allocation,
            'weighted_avg_er': self.weighted_avg_er,
            'advisory_fee': self.advisory_fee,
            'total_fees': self.weighted_avg_er + self.advisory_fee,
            'holdings': []
        }
        
        for ticker, weight in self.portfolio_weights.items():
            dollar_amount = self.portfolio_dollars[ticker]
            shares = dollar_amount / self.current_prices[ticker]
            summary['holdings'].append({
                'ticker': ticker,
                'dollar_amount': dollar_amount,
                'weight': weight,
                'shares': shares,
                'price': self.current_prices[ticker],
                'expense_ratio': self.expense_ratios[ticker],
                'classification': self.classifications[ticker]
            })
        
        return summary
