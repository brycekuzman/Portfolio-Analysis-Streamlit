# Portfolio Analysis Application

## Overview

This is a financial portfolio analysis application that compares user portfolios against optimized model portfolios. The application analyzes historical performance, projects future returns, and provides detailed fee breakdowns to help users make informed investment decisions. It supports both a command-line interface (via `main.py`) and a web-based Streamlit interface (via `app.py`).

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Structure

**Dual Interface Design**
- **CLI Interface (`main.py`)**: Command-line driven portfolio analysis workflow with matplotlib-based visualizations
- **Web Interface (`app.py`)**: Streamlit-based web application providing interactive portfolio analysis with plotly visualizations
- Both interfaces share the same core analytics engine in the `analytics/` module

**Modular Analytics Engine**
The application follows a separation of concerns pattern with specialized modules:
- `portfolio.py`: Core Portfolio class encapsulating portfolio state and analysis methods
- `performance.py`: Pure calculation functions for returns, statistics, and projections
- `data.py`: Data retrieval layer abstracting yfinance API interactions
- `models.py`: Configuration layer defining model portfolios, growth rates, and fees
- `user_input.py`: Input handling and portfolio matching algorithms
- `reporting.py`: Output formatting and visualization generation

### Data Processing Architecture

**Portfolio Analysis Workflow**
1. User provides portfolio holdings as dollar amounts per ticker
2. System fetches current prices to calculate portfolio weights
3. Historical price data retrieved from Yahoo Finance
4. Returns calculated with fee adjustments (advisory fees + expense ratios)
5. Performance statistics computed (returns, volatility, Sharpe ratio, drawdowns)
6. Portfolio matched against pre-defined model portfolios using cosine similarity
7. Comparative analysis generated between current and recommended model portfolio

**Fee Calculation Strategy**
- Advisory fees applied as daily compounding deductions: `(1 - annual_fee)^(1/252)`
- Expense ratios handled per-ticker and weighted by portfolio allocation
- Separate tracking of returns with and without fees for transparency

**Asset Classification System**
The application maps individual tickers to broader asset classes (US Equities, International Equities, Core Fixed Income, Alternatives) to:
- Enable portfolio-level allocation analysis
- Support model portfolio matching based on asset class similarity
- Calculate asset class-specific projections using configured growth rates

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
- Projects multi-year scenarios to compare current vs model portfolios
- Accounts for ongoing fee impacts on long-term returns

**Model Portfolio Strategy**
The application defines five risk-based model portfolios (Conservative to Aggressive) using standard ETFs:
- VOO: US Equities (S&P 500)
- VXUS: International Equities
- BND: Core Fixed Income (Bonds)
- VNQ: Alternatives (Real Estate)

Model portfolios use a standardized low advisory fee (0.25%) to demonstrate fee savings potential.

### Streamlit Web Interface Features

**Modern Design**
The web interface (`app.py`) provides a clean, minimalist dashboard with:
- Custom CSS styling for professional appearance
- Wide layout optimized for data visualization
- Interactive Plotly charts for forward projections and comparisons

**Key Visualizations**
1. **10-Year Forward Projections**: Line chart comparing portfolio growth trajectories
2. **Fee Comparison Charts**: Bar charts showing annual and 10-year cumulative fee differences
3. **Historical Performance**: Interactive growth chart and metrics table
4. **Asset Allocation**: Side-by-side pie charts for current vs model portfolios

**User Interactions**
- Dynamic portfolio input with add/remove ticker functionality
- Adjustable advisory fee settings
- Automatic model portfolio recommendation based on asset similarity
- Expandable sections for detailed breakdowns

## External Dependencies

### Financial Data APIs

**Yahoo Finance (yfinance)**
- Primary data source for historical and current price data
- Provides adjusted close prices accounting for splits and dividends
- No authentication required (public data)
- Rate limiting may apply for high-frequency requests

### Python Libraries

**Data Processing**
- `pandas`: DataFrame operations for time-series financial data
- `numpy`: Numerical computations for returns, statistics, and projections

**Visualization**
- `matplotlib`: Static charts for CLI interface
- `plotly`: Interactive charts for Streamlit web interface
- Both libraries used for portfolio performance and comparison visualizations

**Web Framework**
- `streamlit`: Web application framework providing the interactive UI layer
- Configured with wide layout and collapsed sidebar for optimal chart viewing

### Configuration Data

**Model Portfolios**
Hard-coded model portfolio allocations and parameters in `models.py`:
- Five risk-based portfolio templates
- Asset class growth rate assumptions
- Asset class volatility parameters
- Model advisory fee configuration

**No Database**
The application operates entirely in-memory with no persistent storage. Portfolio data provided per-session by users, and all historical data fetched on-demand from external APIs.