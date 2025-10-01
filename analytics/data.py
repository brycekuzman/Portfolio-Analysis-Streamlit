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


def validate_ticker(ticker):
    """Validate if a ticker exists and return its info."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Check if we got valid data
        if not info or 'symbol' not in info:
            return False, None
        
        return True, info
    except Exception as e:
        return False, None


def get_investment_name(ticker):
    """Get the full name of an investment."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Try different possible keys for the name
        if 'longName' in info:
            return info['longName']
        elif 'shortName' in info:
            return info['shortName']
        elif 'name' in info:
            return info['name']
        else:
            return ticker
    except Exception as e:
        return ticker


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
            # Convert from percentage (e.g., 0.07) to decimal (e.g., 0.0007)
            if expense_ratio is not None:
                expense_ratios[ticker] = expense_ratio / 100.0
            else:
                expense_ratios[ticker] = 0.0
                
        except Exception as e:
            print(f"Could not fetch expense ratio for {ticker}: {e}")
            expense_ratios[ticker] = 0.0
    
    return expense_ratios


def classify_investment(ticker):
    """Classify investment into US Stock, International Stock, US Bond, or International Bond."""
    
    # Common patterns for automatic classification
    us_equity_patterns = ['SPY', 'QQQ', 'VTI', 'VOO', 'IWM', 'DIA', 'IEUR', 'PULS', 'VNQ']
    intl_equity_patterns = ['VXUS', 'VEA', 'VWO', 'IEFA', 'IEMG', 'EFA', 'EEM']
    us_bond_patterns = ['AGG', 'BND', 'VGIT', 'VGLT', 'TLT', 'SHY', 'IEF']
    intl_bond_patterns = ['BNDX', 'IAGG', 'BWX']
    
    # Check for common patterns first
    if ticker in us_equity_patterns:
        return "US Stock"
    elif ticker in intl_equity_patterns:
        return "International Stock"
    elif ticker in us_bond_patterns:
        return "US Bond"
    elif ticker in intl_bond_patterns:
        return "International Bond"
    
    # Try to get info from yfinance
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Check category based on yfinance data
        category = info.get('category', '').lower()
        fund_family = info.get('fundFamily', '').lower()
        asset_class = info.get('assetClass', '').lower()
        
        # US Equity indicators
        if any(keyword in category for keyword in ['large blend', 'large growth', 'large value', 'mid blend', 'mid growth', 'mid value', 'small blend', 'small growth', 'small value']):
            return "US Stock"
        elif 'equity' in category and ('us' in category or 'domestic' in category):
            return "US Stock"
        elif 'reit' in category.lower() or 'real estate' in category.lower():
            return "US Stock"
        elif ticker.endswith('.TO') or ticker.endswith('.L') or ticker.endswith('.F'):
            return "International Stock"
        
        # International Equity indicators
        elif any(keyword in category for keyword in ['foreign', 'international', 'emerging', 'developed', 'europe', 'asia', 'pacific']):
            return "International Stock"
        elif 'equity' in category and any(keyword in category for keyword in ['intl', 'global', 'world']):
            return "International Stock"
        
        # Bond indicators - check if international
        elif any(keyword in category for keyword in ['bond', 'fixed', 'treasury', 'corporate bond', 'government']):
            if any(keyword in category for keyword in ['international', 'global', 'foreign', 'world']):
                return "International Bond"
            else:
                return "US Bond"
        elif 'bond' in asset_class or 'fixed' in asset_class:
            return "US Bond"
        
        # If it's a stock (not fund), classify based on exchange/country
        elif info.get('quoteType') == 'EQUITY':
            country = info.get('country', '').lower()
            if country in ['united states', 'usa', 'us']:
                return "US Stock"
            elif country and country not in ['united states', 'usa', 'us']:
                return "International Stock"
        
    except Exception as e:
        print(f"Could not fetch classification info for {ticker}: {e}")
    
    # If we can't determine automatically, return None to prompt user
    return None


def get_investment_classifications(tickers, overrides=None):
    """Get classifications for all investments, using overrides if provided."""
    classifications = {}
    overrides = overrides or {}
    
    for ticker in tickers:
        # Check if user has overridden the classification
        if ticker in overrides:
            classifications[ticker] = overrides[ticker]
        else:
            auto_classification = classify_investment(ticker)
            
            if auto_classification:
                classifications[ticker] = auto_classification
            else:
                # Default to US Stock if cannot classify
                classifications[ticker] = "US Stock"
    
    return classifications
