import yfinance as yf
import pandas as pd


def get_available_date_range(tickers, start, end):
    """Find the common date range where all tickers have data."""
    latest_start = start
    
    for ticker in tickers:
        # Get a small sample to find actual start date
        sample = yf.download(ticker, start=start, end=end, auto_adjust=True, prepost=True, threads=True)
        if not sample.empty:
            actual_start = sample.index[0].strftime('%Y-%m-%d')
            if actual_start > latest_start:
                latest_start = actual_start
    
    return latest_start, end


def get_price_data(tickers, start, end):
    """Download adjusted close prices for tickers."""
    # Find common date range
    actual_start, actual_end = get_available_date_range(tickers, start, end)
    
    if actual_start != start:
        print(f"Note: Adjusted start date from {start} to {actual_start} due to limited data availability")
    
    data = yf.download(tickers, start=actual_start, end=actual_end, auto_adjust=True, prepost=True, threads=True)
    
    # Handle single vs multiple tickers
    if len(tickers) == 1:
        # For single ticker, data structure is different
        if 'Close' in data.columns:
            prices = data['Close']
        else:
            prices = data
    else:
        # For multiple tickers, extract Close prices
        if 'Close' in data.columns.get_level_values(0):
            prices = data['Close']
        else:
            # Fallback to Adj Close if available
            prices = data['Adj Close']
    
    return prices


def get_current_prices(tickers):
    """Get current prices for tickers to calculate portfolio weights."""
    data = yf.download(tickers, period="1d", interval="1d", auto_adjust=True, prepost=True, threads=True)
    
    if len(tickers) == 1:
        # For single ticker
        current_price = data['Close'].iloc[-1]
        return {tickers[0]: current_price}
    else:
        # For multiple tickers
        current_prices = {}
        for ticker in tickers:
            current_prices[ticker] = data['Close'][ticker].iloc[-1]
        return current_prices


def get_expense_ratios(tickers):
    """Get expense ratios for ETFs, Mutual Funds, and SMAs from yfinance."""
    expense_ratios = {}
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Try different possible keys for expense ratio
            expense_ratio = None
            if 'expenseRatio' in info:
                expense_ratio = info['expenseRatio']
            elif 'annualReportExpenseRatio' in info:
                expense_ratio = info['annualReportExpenseRatio']
            elif 'netExpenseRatio' in info:
                expense_ratio = info['netExpenseRatio']
            
            # If found, store it; otherwise default to 0
            if expense_ratio is not None and expense_ratio > 0:
                expense_ratios[ticker] = expense_ratio
            else:
                expense_ratios[ticker] = 0.0
                
        except Exception as e:
            print(f"Could not fetch expense ratio for {ticker}: {e}")
            expense_ratios[ticker] = 0.0
    
    return expense_ratios
