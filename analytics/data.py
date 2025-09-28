import yfinance as yf
import pandas as pd


def get_price_data(tickers, start, end):
    """Download adjusted close prices for tickers."""
    data = yf.download(tickers, start=start, end=end, auto_adjust=True, prepost=True, threads=True)
    
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
    """Stub for now – hardcoded values, but could later fetch from API."""
    er = {
        "SPY": 0.0009,
        "VOO": 0.0003,
    }
    return {t: er.get(t, 0.0) for t in tickers}
