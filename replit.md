
# Portfolio Analysis Web Application

## Overview

This is a modern, interactive financial portfolio analysis web application built with Streamlit. The application compares user portfolios against optimized model portfolios, analyzing historical performance, projecting future returns, and providing detailed fee breakdowns to help users make informed investment decisions.

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

**Comprehensive Analysis**
1. **10-Year Forward Projections**: Monte Carlo simulations showing portfolio growth trajectories
2. **Fee Comparison**: Annual and cumulative fee analysis with potential savings calculations
3. **Historical Performance**: Actual performance comparison using market data (2015-2025)
4. **Asset Allocation**: Interactive pie charts comparing current vs recommended portfolios
5. **Model Portfolio Matching**: Automatic recommendation based on asset allocation similarity

**Professional Visualizations**
- Plotly interactive charts with hover details
- Side-by-side portfolio comparisons
- Growth trajectory projections
- Fee impact visualizations
- Asset allocation breakdowns

### Data Processing Architecture

**Portfolio Analysis Workflow**
1. User provides portfolio holdings as dollar amounts per ticker
2. System validates tickers and fetches current prices from Yahoo Finance
3. Portfolio weights calculated automatically
4. Historical price data retrieved for performance analysis
5. Returns calculated with fee adjustments (advisory fees + expense ratios)
6. Performance statistics computed (returns, volatility, Sharpe ratio, drawdowns)
7. Portfolio matched against five pre-defined model portfolios using cosine similarity
8. Comparative analysis generated between current and recommended portfolios

**Ticker Validation & Classification**
- Real-time ticker validation using yfinance API
- Automatic investment name lookup and display
- Intelligent asset class classification (US Equities, International Equities, Core Fixed Income, Alternatives)
- User override capability for asset class assignments
- Persistent classification preferences during session

**Fee Calculation Strategy**
- Advisory fees applied as daily compounding deductions: `(1 - annual_fee)^(1/252)`
- Expense ratios handled per-ticker and weighted by portfolio allocation
- Separate tracking of returns with and without fees for transparency
- Annual and 10-year cumulative fee comparisons

**Asset Classification System**
The application maps individual tickers to broader asset classes to:
- Enable portfolio-level allocation analysis
- Support model portfolio matching based on asset class similarity
- Calculate asset class-specific projections using configured growth rates
- Allow manual classification overrides when automatic detection is incorrect

### Data Handling Patterns

**Date Range Normalization**
The system handles data availability mismatches by finding the common date range where all tickers have historical data. This prevents analysis failures when different assets have different data availability windows.

**Single vs Multi-Ticker Handling**
The yfinance API returns different data structures for single tickers vs multiple tickers. The data layer normalizes these differences to provide consistent downstream interfaces.

**Price Data Standardization**
Uses adjusted close prices with auto-adjustment enabled to account for splits and dividends. Falls back to 'Close' when adjusted data unavailable.

### Projection and Modeling

**Future Return Projections**
- Uses configurable growth rates per asset class (defined in `models.py`)
- Applies Monte Carlo simulation with asset class-specific volatility
- Projects 10-year scenarios to compare current vs model portfolios
- Accounts for ongoing fee impacts on long-term returns

**Model Portfolio Strategy**
The application defines five risk-based model portfolios (Conservative to Aggressive) using standard ETFs:
- VOO: US Equities (S&P 500)
- VXUS: International Equities
- BND: Core Fixed Income (Bonds)
- VNQ: Alternatives (Real Estate)

Model portfolios use a standardized low advisory fee (0.25%) to demonstrate fee savings potential.

### Streamlit Web Interface Features

**Modern Minimalist Design**
The web interface provides a clean, professional dashboard with:
- Custom CSS styling for white background and modern typography
- Wide layout optimized for data visualization
- Responsive metric cards and expandable sections
- Intuitive navigation with sidebar summary

**Interactive Components**
1. **Portfolio Input Panel**: Dynamic ticker management with validation feedback
2. **Fee Settings**: Adjustable advisory fee with real-time impact calculations
3. **Asset Class Overrides**: Manual classification adjustment when needed
4. **Navigation Sidebar**: Quick links to all analysis sections with portfolio summary

**Key Visualizations**
1. **10-Year Forward Projections**: Line chart comparing portfolio growth trajectories
2. **Fee Comparison Charts**: Bar charts showing annual and 10-year cumulative fee differences
3. **Historical Performance**: Interactive growth chart with performance metrics table
4. **Asset Allocation**: Side-by-side pie charts for current vs model portfolios with consistent color coding

**User Experience**
- Real-time ticker validation with helpful error messages
- Automatic portfolio value calculations
- One-click analysis with comprehensive results
- Expandable sections for detailed breakdowns
- Professional disclaimers and educational content

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

**Model Portfolios**
Hard-coded model portfolio allocations and parameters in `models.py`:
- Five risk-based portfolio templates (Conservative to Aggressive)
- Asset class growth rate assumptions
- Asset class volatility parameters for Monte Carlo simulations
- Model advisory fee configuration (0.25% standard)

**No Database**
The application operates entirely in-memory with no persistent storage. Portfolio data provided per-session by users, and all historical data fetched on-demand from external APIs. Session state managed through Streamlit's built-in session management.

## Running the Application

The application runs on port 5000 using Streamlit:
```bash
streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true
```

Access the web interface through the Replit webview or via the exposed port.
