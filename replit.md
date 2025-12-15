
# Portfolio Analysis Web Application

## Overview

A clean, modern web app that helps you analyze your investment portfolio. It compares your portfolio against 5 professionally-designed model portfolios, shows you how they've performed historically, projects future growth, and breaks down how much you're paying in fees.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Structure

**Web-First Design**
- **Primary Interface (`app.py`)**: Streamlit-based web application with interactive portfolio analysis and plotly visualizations
- **Analytics Engine (`analytics/`)**: Modular backend providing portfolio analysis, data retrieval, and performance calculations
- Clean, minimalist UI optimized for data visualization and user interaction

**Modular Analytics Engine**
The application follows a separation of concerns pattern with specialized modules:
- `portfolio.py`: Core Portfolio class encapsulating portfolio state and analysis methods
- `performance.py`: Pure calculation functions for returns, statistics, and projections
- `data.py`: Data retrieval layer with ticker validation and yfinance API interactions
- `models.py`: Configuration layer defining model portfolios, growth rates, and fees
- `user_input.py`: Portfolio matching algorithms using cosine similarity
- `reporting.py`: Visualization generation utilities

### Key Features

**Interactive Portfolio Input**
- Dynamic ticker entry with real-time validation
- Automatic investment name lookup
- Asset class classification with manual override capability
- Add/remove holdings with live portfolio value updates
- Adjustable advisory fee settings

**Core Analysis Features**
1. **10-Year Projections**: Estimated future growth for your portfolio vs the recommended model
2. **Fee Comparison**: See exactly how much you're paying in fees and potential savings
3. **Historical Performance**: How each portfolio actually performed from 2015 to now
4. **Asset Allocation**: Visual comparison of your holdings vs the recommended model
5. **Smart Recommendations**: Automatically finds which model portfolio best matches your allocation

**Professional Visualizations**
- Plotly interactive charts with hover details
- Side-by-side portfolio comparisons
- Growth trajectory projections
- Fee impact visualizations
- Asset allocation breakdowns

### How It Works

1. You enter your portfolio holdings (tickers and dollar amounts)
2. The app pulls current prices and historical data from Yahoo Finance
3. Calculates your portfolio weights and asset allocation
4. Compares your allocation to 5 model portfolios and recommends the best match
5. Shows historical performance from 2015 to now with fee deductions
6. Projects 10-year growth based on asset class growth rates
7. Calculates fee savings if you switched to the recommended model

**Fee Calculation Strategy**
- Advisory fees applied as daily compounding deductions: `(1 - annual_fee)^(1/252)`
- Expense ratios handled per-ticker and weighted by portfolio allocation
- Separate tracking of returns with and without fees for transparency
- Annual and 10-year cumulative fee comparisons

**Asset Classification**
Tickers are automatically classified into: US Equities, International Equities, Core Fixed Income, or Alternatives. This enables better portfolio matching and growth projections based on asset class characteristics.

### Projections & Models

**10-Year Projections**
- Based on historical average growth rates for each asset class (US Equities: 9%, International: 8%, Bonds: 3.5%, Alternatives: 11%)
- Accounts for advisory fees and expense ratios as they compound over time
- Shows year-by-year estimated growth assuming current allocations continue

**5 Model Portfolios**
- **Conservative**: 15% VOO, 20% VXUS, 60% BND, 5% VNQ
- **Moderately Conservative**: 25% VOO, 25% VXUS, 40% BND, 10% VNQ
- **Balanced**: 30% VOO, 25% VXUS, 30% BND, 15% VNQ
- **Moderately Aggressive**: 40% VOO, 20% VXUS, 15% BND, 25% VNQ
- **Aggressive**: 50% VOO, 15% VXUS, 0% BND, 35% VNQ

All model portfolios use a 0.25% advisory fee.

### Web Interface

**Clean, Minimalist Design**
- Simple input form to add/remove holdings and set advisory fee
- Professional Plotly charts with hover details
- One-click "Analyze Portfolio" button
- Expandable sections for detailed breakdowns

**Visualizations**
- 10-Year Growth Projection (line chart)
- Annual & 10-Year Fee Comparison (bar charts)
- Historical Performance Chart
- Asset Allocation Pie Charts

## External Dependencies

### Financial Data APIs

**Yahoo Finance (yfinance)**
- Primary data source for historical and current price data
- Ticker validation and investment name lookup
- Provides adjusted close prices accounting for splits and dividends
- No authentication required (public data)
- Rate limiting may apply for high-frequency requests

### Python Libraries

**Data Processing**
- `pandas`: DataFrame operations for time-series financial data
- `numpy`: Numerical computations for returns, statistics, and projections

**Visualization**
- `plotly`: Interactive charts for web interface
- `matplotlib`: Utility support for data visualization

**Web Framework**
- `streamlit`: Web application framework providing the interactive UI layer
- Configured with wide layout and custom CSS for optimal user experience

### Configuration Data

**Data Storage**
No database - everything runs in-memory. Portfolio data is entered each session, and all historical data is fetched live from Yahoo Finance via API.

## Running the Application

The application runs on port 5000 using Streamlit:
```bash
streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true
```

Access the web interface through the Replit webview or via the exposed port.
