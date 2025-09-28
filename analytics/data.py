import yfinance as yf
import pandas as pd


def get_price_data(tickers, start, end):
    """Download adjusted close prices for tickers."""
    prices = yf.download(tickers, start=start, end=end)["Adj Close"]
    return prices


def get_expense_ratios(tickers):
    """Stub for now – hardcoded values, but could later fetch from API."""
    er = {
        "SPY": 0.0009,
        "VOO": 0.0003,
    }
    return {t: er.get(t, 0.0) for t in tickers}
