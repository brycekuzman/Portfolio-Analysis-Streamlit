
import yfinance as yf
from datetime import datetime, timedelta
from functools import wraps
import time

# Simple in-memory cache with TTL
_cache = {}
_cache_timestamps = {}

def cache_with_ttl(ttl_seconds=300):
    """Decorator to cache function results with time-to-live."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            
            # Check if cached and not expired
            if cache_key in _cache:
                cached_time = _cache_timestamps.get(cache_key, 0)
                if time.time() - cached_time < ttl_seconds:
                    return _cache[cache_key]
            
            # Call function and cache result
            result = func(*args, **kwargs)
            _cache[cache_key] = result
            _cache_timestamps[cache_key] = time.time()
            
            return result
        return wrapper
    return decorator

def clear_cache():
    """Clear all cached data."""
    _cache.clear()
    _cache_timestamps.clear()

def get_ticker_info_batch(tickers):
    """Fetch ticker info for multiple tickers in a single optimized call."""
    info_dict = {}
    
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info_dict[ticker] = stock.info
        except Exception as e:
            info_dict[ticker] = None
    
    return info_dict
