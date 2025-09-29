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
    """Classify investment into US Equities, International Equities, Core Fixed Income, or Alternatives."""
    
    # Common patterns for automatic classification
    us_equity_patterns = ['SPY', 'QQQ', 'VTI', 'VOO', 'IWM', 'DIA']
    intl_equity_patterns = ['VXUS', 'VEA', 'VWO', 'IEFA', 'IEMG', 'EFA', 'EEM']
    fixed_income_patterns = ['AGG', 'BND', 'VGIT', 'VGLT', 'TLT', 'SHY', 'IEF']
    
    # Check for common patterns first
    if ticker in us_equity_patterns:
        return "US Equities"
    elif ticker in intl_equity_patterns:
        return "International Equities"
    elif ticker in fixed_income_patterns:
        return "Core Fixed Income"
    
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
            return "US Equities"
        elif 'equity' in category and ('us' in category or 'domestic' in category):
            return "US Equities"
        elif ticker.endswith('.TO') or ticker.endswith('.L') or ticker.endswith('.F'):
            return "International Equities"
        
        # International Equity indicators
        elif any(keyword in category for keyword in ['foreign', 'international', 'emerging', 'developed', 'europe', 'asia', 'pacific']):
            return "International Equities"
        elif 'equity' in category and any(keyword in category for keyword in ['intl', 'global', 'world']):
            return "International Equities"
        
        # Fixed Income indicators
        elif any(keyword in category for keyword in ['bond', 'fixed', 'treasury', 'corporate bond', 'government']):
            return "Core Fixed Income"
        elif 'bond' in asset_class or 'fixed' in asset_class:
            return "Core Fixed Income"
        
        # If it's a stock (not fund), classify based on exchange/country
        elif info.get('quoteType') == 'EQUITY':
            country = info.get('country', '').lower()
            if country in ['united states', 'usa', 'us']:
                return "US Equities"
            elif country and country not in ['united states', 'usa', 'us']:
                return "International Equities"
        
    except Exception as e:
        print(f"Could not fetch classification info for {ticker}: {e}")
    
    # If we can't determine automatically, return None to prompt user
    return None


def get_investment_classifications(tickers):
    """Get classifications for all investments, prompting user for unknown ones."""
    classifications = {}
    
    for ticker in tickers:
        auto_classification = classify_investment(ticker)
        
        if auto_classification:
            classifications[ticker] = auto_classification
        else:
            # Prompt user for classification
            print(f"\nCould not automatically classify {ticker}.")
            print("Please select the classification:")
            print("1. US Equities")
            print("2. International Equities") 
            print("3. Core Fixed Income")
            print("4. Alternatives")
            
            while True:
                try:
                    choice = input(f"Enter choice (1-4) for {ticker}: ").strip()
                    if choice == '1':
                        classifications[ticker] = "US Equities"
                        break
                    elif choice == '2':
                        classifications[ticker] = "International Equities"
                        break
                    elif choice == '3':
                        classifications[ticker] = "Core Fixed Income"
                        break
                    elif choice == '4':
                        classifications[ticker] = "Alternatives"
                        break
                    else:
                        print("Invalid choice. Please enter 1, 2, 3, or 4.")
                except KeyboardInterrupt:
                    print(f"\nDefaulting {ticker} to 'Alternatives'")
                    classifications[ticker] = "Alternatives"
                    break
    
    return classifications
