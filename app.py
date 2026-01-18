import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from analytics.portfolio import Portfolio
from analytics.user_input import find_best_matching_model
from analytics.models import model_portfolios, model_fee

# Page configuration
st.set_page_config(
    page_title="Portfolio Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern minimalist design with white background
st.markdown("""
    <style>
    /* Force light theme */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }

    /* Main content area */
    .main {
        padding: 0.2rem 1rem !important;
        background-color: #ffffff;
        color: #000000;
    }

    /* Typography */
    h1 {
        font-weight: 300;
        font-size: 1.5rem !important;
        margin-top: 0 !important;
        margin-bottom: 0.05rem !important;
        color: #000000;
        letter-spacing: -0.02em;
    }
    h2 {
        font-weight: 300;
        font-size: 1.2rem !important;
        margin-top: 0.4rem !important;
        margin-bottom: 0.2rem !important;
        color: #1a1a1a;
        border-bottom: 1px solid #e5e5e5;
        padding-bottom: 0.05rem !important;
    }
    h3 {
        font-weight: 400;
        font-size: 1rem !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.1rem !important;
        color: #2a2a2a;
    }

    /* Buttons */
    .stButton>button {
        background-color: #4A90E2;
        color: #ffffff;
        border-radius: 6px;
        padding: 0.3rem 1.5rem !important;
        font-weight: 500;
        border: none;
        transition: all 0.2s ease;
        font-size: 0.85rem !important;
        letter-spacing: 0.02em;
    }
    .stButton>button:hover {
        background-color: #357ABD;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
    }

    /* Primary button styling */
    .stButton>button[kind="primary"] {
        background-color: #4A90E2;
        color: #ffffff;
    }
    .stButton>button[kind="primary"]:hover {
        background-color: #357ABD;
    }

    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.1rem !important;
        color: #000000;
        font-weight: 600;
        line-height: 1 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #4a4a4a;
        font-size: 0.75rem !important;
        font-weight: 500;
        margin-bottom: 0 !important;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 0.7rem !important;
    }

    /* Metric cards */
    .metric-card {
        background-color: #fafafa;
        padding: 0.4rem !important;
        border-radius: 6px;
        border-left: 3px solid #000000;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Input fields */
    .stTextInput>div>div>input {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #d0d0d0;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: border-color 0.2s ease;
    }
    .stTextInput>div>div>input:focus {
        border-color: #4A90E2;
        outline: none;
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
    }
    .stNumberInput>div>div>input {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #d0d0d0 !important;
        border-radius: 6px;
        padding: 0.75rem 1rem;
        font-size: 0.95rem;
        transition: border-color 0.2s ease;
    }
    .stNumberInput>div>div>input:focus {
        border-color: #4A90E2 !important;
        outline: none;
        box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
    }

    /* Force number input controls to be visible */
    .stNumberInput button {
        color: #000000 !important;
        background-color: #f0f0f0 !important;
    }

    /* Force number input text area to be white */
    .stNumberInput input[type="number"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Target all input elements within number input containers */
    div[data-baseweb="input"] input {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Fix selectbox/dropdown background */
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Dataframes */
    .stDataFrame {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .stDataFrame table {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .stDataFrame th {
        background-color: #f0f0f0 !important;
        color: #000000 !important;
        font-weight: 600;
    }
    .stDataFrame td {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Additional dataframe selectors */
    div[data-testid="stDataFrame"] {
        background-color: #ffffff !important;
    }
    div[data-testid="stDataFrame"] table {
        background-color: #ffffff !important;
    }
    div[data-testid="stDataFrame"] tbody tr {
        background-color: #ffffff !important;
    }
    div[data-testid="stDataFrame"] tbody td {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    div[data-testid="stDataFrame"] thead th {
        background-color: #f0f0f0 !important;
        color: #000000 !important;
    }

    /* Force all table elements to have white background and black text */
    table, table * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    thead, thead * {
        background-color: #f0f0f0 !important;
        color: #000000 !important;
    }

    /* Target styled dataframes specifically */
    [data-testid="stDataFrame"] div[class*="glideDataEditor"] {
        background-color: #ffffff !important;
    }
    [data-testid="stDataFrame"] div[class*="glideDataEditor"] * {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* Sidebar (if used) */
    .css-1d391kg {
        background-color: #f8f9fa;
        color: #000000;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border: 1px solid #e5e5e5;
        color: #000000;
    }
    .streamlit-expanderContent {
        background-color: #ffffff;
        color: #000000;
    }

    /* Clean spacing */
    .element-container {
        margin-bottom: 0.15rem !important;
    }

    /* Reduce default streamlit vertical padding */
    .block-container {
        padding-top: 0.1rem !important;
        padding-bottom: 0.1rem !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }

    /* Streamlit specific spacing overrides */
    div.stVerticalBlock > div {
        padding-top: 0 !important;
        padding-bottom: 0.05rem !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem !important;
    }
    
    /* Horizontal lines */
    hr {
        margin-top: 0.25rem !important;
        margin-bottom: 0.25rem !important;
    }

    /* Remove any dark theme remnants */
    div[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        color: #000000;
    }

    /* All text elements */
    .stMarkdown, .stMarkdown p, .stMarkdown div {
        color: #000000;
    }

    /* Caption text */
    .caption {
        color: #6a6a6a;
        font-size: 0.85rem;
    }

    /* Headers with better spacing */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        margin-top: 2rem;
        color: #000000;
    }

    /* Remove button outlines on focus */
    .stButton>button:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(0,0,0,0.1);
    }

    /* Delete button sizing to match input fields */
    .stButton button[kind="secondary"] {
        height: 38px !important;
        min-height: 38px !important;
        max-height: 38px !important;
        padding: 0.5rem 0.75rem !important;
        line-height: 1 !important;
    }

    /* Fix all text to be black */
    * {
        color: #000000 !important;
    }

    /* Override plotly defaults */
    .js-plotly-plot {
        background-color: #ffffff !important;
    }

    /* Reduce sidebar spacing */
    div[data-testid="stSidebar"] .element-container {
        margin-bottom: 0.25rem !important;
    }
    div[data-testid="stSidebar"] h3 {
        margin-top: 0.25rem !important;
        margin-bottom: 0.25rem !important;
        font-size: 1.1rem !important;
    }
    div[data-testid="stSidebar"] .stMarkdown {
        margin-bottom: 0.15rem !important;
        margin-top: 0.15rem !important;
    }
    div[data-testid="stSidebar"] hr {
        margin-top: 0.25rem !important;
        margin-bottom: 0.25rem !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stMetric"] {
        margin-bottom: 0.15rem !important;
        padding-bottom: 0 !important;
    }
    div[data-testid="stSidebar"] div[data-testid="stMetricValue"] {
        margin-bottom: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {"IEUR": 20000, "VOO": 10000, "PULS": 10000}
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

# Sidebar Navigation
with st.sidebar:
    # Portfolio Summary first
    st.markdown("### Portfolio Summary")
    total_value = sum(st.session_state.portfolio.values())
    st.metric("Total Value", f"${total_value:,.0f}")
    st.metric("Holdings", len([t for t in st.session_state.portfolio.keys() if t.strip()]))
    
    st.markdown("---")
    
    # Navigation links
    st.markdown("### Navigation")
    st.markdown("[📝 Portfolio Input](#enter-portfolio-information)")
    
    if st.session_state.analyzed:
        st.markdown("[🎯 Recommended Portfolio](#recommended-" + st.session_state.model_name.lower().replace(" ", "-") + "-portfolio)")
        st.markdown("[📚 All Model Portfolios](#all-model-portfolios)")
        st.markdown("[🎯 Asset Allocation](#asset-allocation)")
        st.markdown("[📈 10-Year Projections](#10-year-forward-projections)")
        st.markdown("[💰 Fee Comparison](#projected-fees-savings)")
        st.markdown("[📊 Historical Performance](#historical-performance)")

# Professional Header
st.markdown("""
    <div style="text-align: center; padding: 1rem 0 0.5rem 0; border-bottom: 2px solid #4A90E2;">
        <h1 style="font-size: 2.2rem; font-weight: 300; margin-bottom: 0.25rem; color: #1a1a1a;">
            📊 Portfolio Analyzer
        </h1>
        <p style="font-size: 1rem; color: #6a6a6a; margin-top: 0;">
            Backtest your portfolio, find the best model, and optimize your fees
        </p>
    </div>
""", unsafe_allow_html=True)

# Remove the extra <br>
# st.markdown("<br>", unsafe_allow_html=True)

# Portfolio Input Section
st.markdown("""
    <div style="margin-top: 1rem; padding: 0.5rem 0; border-bottom: 1px solid #e5e5e5;">
        <h2 style="font-size: 1.6rem; font-weight: 400; color: #1a1a1a; margin: 0;">
            📝 Portfolio Input
        </h2>
        <p style="color: #6a6a6a; margin-top: 0.25rem; font-size: 0.9rem;">
            Enter your investment holdings and the advisory fee paid to manage these investments. The analysis will determine the best matching model portfolio and provide a detailed comparison.
        </p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state for asset class overrides
if 'asset_class_overrides' not in st.session_state:
    st.session_state.asset_class_overrides = {}

# Callback function to handle ticker changes
def handle_ticker_change(old_ticker):
    """Handle when a ticker is changed to trigger rerun."""
    pass  # The rerun will happen in the main logic

# Settings Section
st.markdown("""
    <h3 style="font-size: 1.2rem; font-weight: 500; color: #2a2a2a; margin-top: 1rem; margin-bottom: 0.5rem;">
        ⚙️ Advisory Fee
    </h3>
""", unsafe_allow_html=True)
col_settings1, col_settings2, col_settings3 = st.columns([1, 1, 2])

with col_settings1:
    advisory_fee = st.number_input(
        "Annual Advisory Fee (%)", 
        min_value=0.0, 
        max_value=5.0, 
        value=1.0, 
        step=0.05,
        help="Your current advisory fee percentage"
    ) / 100

with col_settings2:
    total_value = sum(st.session_state.portfolio.values())
    st.metric("Total Portfolio Value", f"${total_value:,.0f}")

st.markdown("<br>", unsafe_allow_html=True)

# E*TRADE Account Integration Section
st.markdown("""
    <h3 style="font-size: 1.2rem; font-weight: 500; color: #2a2a2a; margin-top: 1rem; margin-bottom: 0.5rem;">
        🔗 Import from E*TRADE
    </h3>
""", unsafe_allow_html=True)

# Initialize session state for E*TRADE
if 'etrade_accounts' not in st.session_state:
    st.session_state.etrade_accounts = []
if 'etrade_authenticated' not in st.session_state:
    st.session_state.etrade_authenticated = False

import os
from analytics.etrade_client import ETradeClient

# Initialize session state for E*TRADE auth flow
if 'etrade_auth_url' not in st.session_state:
    st.session_state.etrade_auth_url = None
if 'etrade_awaiting_verifier' not in st.session_state:
    st.session_state.etrade_awaiting_verifier = False
if 'etrade_request_token' not in st.session_state:
    st.session_state.etrade_request_token = None
if 'etrade_request_token_secret' not in st.session_state:
    st.session_state.etrade_request_token_secret = None

# E*TRADE Authentication
consumer_key = os.getenv("ETRADE_CONSUMER_KEY")
consumer_secret = os.getenv("ETRADE_CONSUMER_SECRET")
oauth_token = os.getenv("ETRADE_OAUTH_TOKEN")
oauth_token_secret = os.getenv("ETRADE_OAUTH_TOKEN_SECRET")
use_sandbox = os.getenv("ETRADE_SANDBOX", "true").lower() == "true"

if consumer_key and consumer_secret:
    try:
        etrade_client = ETradeClient(consumer_key, consumer_secret, sandbox=use_sandbox)
        
        # Restore request token if we're in the middle of auth flow
        if st.session_state.etrade_request_token and st.session_state.etrade_request_token_secret:
            etrade_client.oauth_token = st.session_state.etrade_request_token
            etrade_client.oauth_token_secret = st.session_state.etrade_request_token_secret
        
        # If we have saved tokens, try to use them
        if oauth_token and oauth_token_secret and not st.session_state.etrade_awaiting_verifier:
            etrade_client.set_access_token(oauth_token, oauth_token_secret)
            st.session_state.etrade_authenticated = True
        
        # Fetch accounts if authenticated
        if st.session_state.etrade_authenticated and not st.session_state.etrade_accounts:
            try:
                accounts_data = etrade_client.list_accounts()
                if 'AccountListResponse' in accounts_data:
                    accounts = accounts_data['AccountListResponse'].get('Accounts', {}).get('Account', [])
                    if not isinstance(accounts, list):
                        accounts = [accounts]
                    
                    st.session_state.etrade_accounts = [
                        {
                            'account_id': acc.get('accountId', 'Unknown'),
                            'account_id_key': acc.get('accountIdKey', ''),
                            'account_name': acc.get('accountName', 'Unknown'),
                            'account_type': acc.get('accountType', 'Unknown')
                        }
                        for acc in accounts
                    ]
            except Exception as e:
                error_msg = str(e)
                if "401" in error_msg:
                    st.warning("⚠️ E*TRADE session expired. Please re-authenticate below.")
                    st.session_state.etrade_authenticated = False
                    st.session_state.etrade_accounts = []
                else:
                    st.error(f"Error fetching E*TRADE accounts: {error_msg}")
        
        # Re-authentication flow
        if not st.session_state.etrade_authenticated or not st.session_state.etrade_accounts:
            if st.button("🔄 Start Authentication", use_container_width=True):
                    try:
                        # Get request token
                        request_token, request_token_secret = etrade_client.get_request_token()
                        # Store in session state
                        st.session_state.etrade_request_token = request_token
                        st.session_state.etrade_request_token_secret = request_token_secret
                        # Get authorization URL
                        auth_url = etrade_client.get_authorization_url()
                        st.session_state.etrade_auth_url = auth_url
                        st.session_state.etrade_awaiting_verifier = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error starting authentication: {str(e)}")
            
            # Show authorization URL and verifier input if we're in auth flow
            if st.session_state.etrade_awaiting_verifier and st.session_state.etrade_auth_url:
                st.markdown("**Step 1:** Click the link below to authorize:")
                st.markdown(f"[Open E*TRADE Authorization]({st.session_state.etrade_auth_url})")
                
                st.markdown("**Step 2:** After authorizing, enter the verification code:")
                verifier_code = st.text_input("Verification Code", key="etrade_verifier")
                
                if st.button("✅ Complete Authentication", disabled=not verifier_code, use_container_width=True):
                    try:
                        # Exchange verifier for access token (using stored request token)
                        new_token, new_token_secret = etrade_client.get_access_token(verifier_code)
                        
                        st.success(f"✅ Authentication successful! Please update your Secrets:")
                        st.code(f"ETRADE_OAUTH_TOKEN: {new_token}\nETRADE_OAUTH_TOKEN_SECRET: {new_token_secret}")
                        
                        st.warning("📝 **Next Steps:**")
                        st.markdown("1. Copy the tokens above")
                        st.markdown("2. Open the Secrets tool (🔒 in the left sidebar)")
                        st.markdown("3. Update `ETRADE_OAUTH_TOKEN` and `ETRADE_OAUTH_TOKEN_SECRET`")
                        st.markdown("4. **Stop and restart the app** using the Stop/Run buttons at the top")
                        
                        st.info("⚠️ The app must be restarted to load the new tokens from Secrets.")
                        
                        # Reset auth flow
                        st.session_state.etrade_auth_url = None
                        st.session_state.etrade_awaiting_verifier = False
                        st.session_state.etrade_request_token = None
                        st.session_state.etrade_request_token_secret = None
                    except Exception as e:
                        st.error(f"Error completing authentication: {str(e)}")
        
        # Display account selector if we have accounts
        elif st.session_state.etrade_accounts:
            account_options = [
                f"{acc['account_name']} ({acc['account_id']}) - {acc['account_type']}"
                for acc in st.session_state.etrade_accounts
            ]
            
            selected_accounts = st.multiselect(
                "Select E*TRADE Account(s)",
                options=account_options,
                help="Select one or more accounts to import holdings"
            )
            
            if st.button("📥 Import Holdings from E*TRADE", use_container_width=True):
                if selected_accounts:
                    import_placeholder = st.empty()
                    import_placeholder.info("🔄 Importing holdings from E*TRADE...")
                    
                    try:
                        # Get selected account keys
                        selected_indices = [account_options.index(acc) for acc in selected_accounts]
                        selected_account_keys = [
                            st.session_state.etrade_accounts[i]['account_id_key']
                            for i in selected_indices
                        ]
                        
                        # Fetch holdings
                        holdings = etrade_client.get_holdings_summary(selected_account_keys)
                        
                        # Clear current portfolio
                        st.session_state.portfolio = {}
                        st.session_state.asset_class_overrides = {}
                        
                        # Aggregate holdings by symbol
                        symbol_values = {}
                        for holding in holdings:
                            symbol = holding['symbol']
                            market_value = round(holding['market_value'])  # Round to nearest whole number
                            
                            if symbol in symbol_values:
                                symbol_values[symbol] += market_value
                            else:
                                symbol_values[symbol] = market_value
                        
                        # Update portfolio
                        st.session_state.portfolio = symbol_values
                        
                        import_placeholder.success(f"✅ Successfully imported {len(symbol_values)} holdings from {len(selected_accounts)} account(s)!")
                        st.rerun()
                    except Exception as e:
                        import_placeholder.error(f"❌ Error importing holdings: {str(e)}")
                else:
                    st.warning("Please select at least one account to import holdings.")
            
            # Add token renewal option
            st.markdown("---")
            if st.button("🔄 Try Token Renewal", use_container_width=True, help="Attempt to renew tokens without full re-authentication"):
                try:
                    if etrade_client.renew_access_token():
                        st.success("Token renewed successfully! Refresh the page to continue.")
                    else:
                        st.error("Token renewal failed. Please use full re-authentication above.")
                except Exception as e:
                    st.error(f"Token renewal error: {str(e)}")
    except Exception as e:
        st.error(f"Error initializing E*TRADE client: {str(e)}")
else:
    st.info("E*TRADE API credentials not found. Add ETRADE_CONSUMER_KEY and ETRADE_CONSUMER_SECRET to Secrets to enable account import.")

st.markdown("<br>", unsafe_allow_html=True)

# Holdings Section
st.markdown("""
    <h3 style="font-size: 1.2rem; font-weight: 500; color: #2a2a2a; margin-top: 1rem; margin-bottom: 0.5rem;">
        💼 Current Holdings
    </h3>
""", unsafe_allow_html=True)

# Import validation and name functions
from analytics.data import validate_ticker, get_investment_name, classify_investment

# Add column headers
header_cols = st.columns([1.5, 2, 2, 2, 0.5])
with header_cols[0]:
    st.markdown("**Investment Symbol**")
with header_cols[1]:
    st.markdown("**Investment Name**")
with header_cols[2]:
    st.markdown("**Current Market Value ($)**")
with header_cols[3]:
    st.markdown("**Asset Class**")
with header_cols[4]:
    st.markdown("**Delete**")

# Display current holdings
for i, (ticker, amount) in enumerate(list(st.session_state.portfolio.items())):
    # Validate ticker only if it's not empty
    is_valid = False
    ticker_info = None
    if ticker.strip():  # Only validate non-empty tickers
        is_valid, ticker_info = validate_ticker(ticker)

    # Create columns for ticker, name, amount, asset class, and delete button
    cols = st.columns([1.5, 2, 2, 2, 0.5])

    with cols[0]:
        new_ticker = st.text_input("Ticker", value=ticker, key=f"ticker_{ticker}_{i}", label_visibility="collapsed", placeholder="Enter ticker...", on_change=lambda t=ticker: handle_ticker_change(t))

    with cols[1]:
        if is_valid:
            investment_name = get_investment_name(ticker)
            st.markdown(f'<input type="text" value="{investment_name}" disabled style="width: 100%; padding: 0.5rem 1rem; border: 1px solid #d0d0d0; border-radius: 6px; background-color: #f5f5f5; color: #000000; font-size: 0.95rem; height: 38px; box-sizing: border-box;">', unsafe_allow_html=True)
        elif ticker.strip():  # Only show invalid message for non-empty tickers
            st.text_input("Name", value="⚠️ Invalid Ticker", key=f"name_{ticker}_{i}", label_visibility="collapsed", disabled=True)
        else:
            st.text_input("Name", value="", key=f"name_{ticker}_{i}", label_visibility="collapsed", disabled=True, placeholder="Enter ticker first...")

    with cols[2]:
        new_amount = st.number_input("Amount", value=float(amount), min_value=0.0, step=1000.0, key=f"amount_{ticker}_{i}", label_visibility="collapsed", format="%.0f")

    with cols[3]:
        if is_valid:
            # Get automatic classification
            auto_classification = classify_investment(ticker)

            # Check if user has overridden the classification
            if ticker in st.session_state.asset_class_overrides:
                default_class = st.session_state.asset_class_overrides[ticker]
            elif auto_classification:
                default_class = auto_classification
            else:
                default_class = "US Stock"

            # Asset class options
            asset_classes = ["US Equities", "International Equities", "Core Fixed Income", "Alternatives"]
            default_index = asset_classes.index(default_class) if default_class in asset_classes else 0

            selected_class = st.selectbox(
                "Asset Class",
                options=asset_classes,
                index=default_index,
                key=f"asset_class_{ticker}_{i}",
                label_visibility="collapsed"
            )

            # Store the override if user changed it
            if auto_classification and selected_class != auto_classification:
                st.session_state.asset_class_overrides[ticker] = selected_class
            elif ticker in st.session_state.asset_class_overrides and selected_class == auto_classification:
                # Remove override if user changed back to automatic classification
                del st.session_state.asset_class_overrides[ticker]
        else:
            st.text_input("Asset Class", value="N/A" if ticker.strip() else "", key=f"asset_class_{ticker}_{i}", label_visibility="collapsed", disabled=True)

    with cols[4]:
        # Use ticker in key to ensure proper alignment
        if st.button("🗑️", key=f"remove_{ticker}_{i}", help="Remove this holding"):
            del st.session_state.portfolio[ticker]
            if ticker in st.session_state.asset_class_overrides:
                del st.session_state.asset_class_overrides[ticker]
            st.rerun()

    # Show warning only for non-empty invalid tickers
    if ticker.strip() and not is_valid:
        st.warning(f"⚠️ '{ticker}' is not a valid investment symbol. Please correct it or remove this holding.")

    # Update portfolio
    if new_ticker.upper() != ticker:
        del st.session_state.portfolio[ticker]
        if ticker in st.session_state.asset_class_overrides:
            if new_ticker.strip():  # Only transfer override if new ticker is not empty
                st.session_state.asset_class_overrides[new_ticker.upper()] = st.session_state.asset_class_overrides.pop(ticker)
            else:
                del st.session_state.asset_class_overrides[ticker]
        st.session_state.portfolio[new_ticker.upper()] = new_amount
        st.rerun()  # Force rerun when ticker changes
    else:
        st.session_state.portfolio[ticker] = new_amount

# Add new holding
st.markdown("")
if st.button("➕ Add Holding", use_container_width=True):
    # Use empty string as ticker placeholder instead of NEWx
    st.session_state.portfolio[""] = 1000.0
    st.rerun()

# Analyze Portfolio button below
st.markdown("")
analyze_clicked = st.button("🔍 Analyze Portfolio", use_container_width=True, type="primary")

st.markdown("")

# Analyze Button
if analyze_clicked:
    # Validate all tickers before analysis
    from analytics.data import validate_ticker
    invalid_tickers = []
    empty_tickers = []
    
    for ticker in st.session_state.portfolio.keys():
        if not ticker.strip():
            empty_tickers.append("(empty)")
        else:
            is_valid, _ = validate_ticker(ticker)
            if not is_valid:
                invalid_tickers.append(ticker)

    if empty_tickers or invalid_tickers:
        error_msg = "❌ Cannot analyze portfolio. "
        if empty_tickers:
            error_msg += f"Please enter ticker symbols for {len(empty_tickers)} empty holding(s). "
        if invalid_tickers:
            error_msg += f"Please correct or remove these invalid tickers: {', '.join(invalid_tickers)}"
        st.error(error_msg)
    else:
        progress_bar = st.progress(0, text="Initializing analysis...")
        try:
            # Step 1: Create portfolios (20%)
            progress_bar.progress(10, text="Creating portfolio objects...")
            
            from concurrent.futures import ThreadPoolExecutor
            from datetime import datetime, timedelta
            
            # Create current portfolio with asset class overrides
            current_portfolio = Portfolio(
                st.session_state.portfolio, 
                "Current", 
                advisory_fee,
                st.session_state.asset_class_overrides
            )
            
            progress_bar.progress(20, text="Finding best matching model...")

            # Find best matching model
            best_match, similarity = find_best_matching_model(current_portfolio.asset_class_allocation)
            model_name, model_allocations = best_match

            # Create model portfolio
            model_portfolio_dollars = {ticker: total_value * weight for ticker, weight in model_allocations.items()}
            model_portfolio = Portfolio(model_portfolio_dollars, model_name, model_fee)
            
            progress_bar.progress(40, text="Analyzing historical performance...")

            # Step 2: Historical analysis - 10 years from today (40%)
            end_date = datetime.today().strftime('%Y-%m-%d')
            start_date = (datetime.today() - timedelta(days=365*10)).strftime('%Y-%m-%d')
            
            # Run historical analysis in parallel
            with ThreadPoolExecutor(max_workers=2) as executor:
                current_future = executor.submit(
                    current_portfolio.analyze_historical_performance, start_date, end_date
                )
                # Wait for current to get actual_start_date
                current_results = current_future.result()
                
                # Now analyze model with same start date
                model_future = executor.submit(
                    model_portfolio.analyze_historical_performance, 
                    current_results['actual_start_date'], 
                    end_date
                )
                model_results = model_future.result()
            
            progress_bar.progress(70, text="Projecting future returns...")

            # Step 3: Future projections (70%)
            with ThreadPoolExecutor(max_workers=4) as executor:
                current_proj_future = executor.submit(current_portfolio.project_future_returns, 10)
                model_proj_future = executor.submit(model_portfolio.project_future_returns, 10)
                current_proj_fees_future = executor.submit(current_portfolio.project_future_with_fees, 10)
                model_proj_fees_future = executor.submit(model_portfolio.project_future_with_fees, 10)
                
                current_projections = current_proj_future.result()
                model_projections = model_proj_future.result()
                current_projections_with_fees = current_proj_fees_future.result()
                model_projections_with_fees = model_proj_fees_future.result()
            
            progress_bar.progress(90, text="Finalizing results...")

                # Step 4: Store in session state (100%)
            st.session_state.current_portfolio = current_portfolio
            st.session_state.model_portfolio = model_portfolio
            st.session_state.model_name = model_name
            st.session_state.similarity = similarity
            st.session_state.current_results = current_results
            st.session_state.model_results = model_results
            st.session_state.current_projections = current_projections
            st.session_state.model_projections = model_projections
            st.session_state.current_projections_with_fees = current_projections_with_fees
            st.session_state.model_projections_with_fees = model_projections_with_fees
            st.session_state.analyzed = True

            progress_bar.progress(100, text="Complete!")
            st.success(f"Analysis complete! Best match: **{model_name}** Portfolio ({similarity:.1%} similarity)")
            st.rerun()

        except Exception as e:
            progress_bar.empty()
            st.error(f"Error during analysis: {str(e)}")
            st.session_state.analyzed = False

# Results Section
if st.session_state.analyzed:
    st.markdown("""
        <div style="margin-top: 3rem; padding: 2rem 0 1rem 0; border-top: 3px solid #4A90E2; background: linear-gradient(to bottom, #f8f9fa 0%, #ffffff 100%);">
            <h2 style="font-size: 2rem; font-weight: 400; color: #1a1a1a; text-align: center; margin-bottom: 0.5rem;">
                🎯 Analysis Results
            </h2>
        </div>
    """, unsafe_allow_html=True)

    # Model Portfolio Info
    st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0 1.5rem 0;">
            <h3 style="font-size: 1.6rem; font-weight: 500; color: #2a2a2a; margin-bottom: 0.5rem;">
                Recommended: {st.session_state.model_name} Portfolio
            </h3>
            <p style="color: #6a6a6a; font-size: 0.95rem;">
                Asset allocation similarity: {st.session_state.similarity:.1%}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Display model allocations
    cols = st.columns(5)
    for i, (ticker, weight) in enumerate(st.session_state.model_portfolio.portfolio_weights.items()):
        with cols[i % 5]:
            st.metric(ticker, f"{weight:.1%}")

    st.markdown("---")

    # All Model Portfolios Reference
    st.markdown("""
        <div style="margin-top: 2.5rem; padding: 1rem 0; border-bottom: 1px solid #e5e5e5;">
            <h2 style="font-size: 1.8rem; font-weight: 400; color: #1a1a1a; margin: 0;">
                📚 All Model Portfolios
            </h2>
            <p style="color: #6a6a6a; margin-top: 0.5rem; font-size: 0.95rem;">
                Review all available model portfolios to see alternative allocations
            </p>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("📊 View All Model Portfolios"):
        # Get all unique tickers across all models
        all_tickers = sorted(set(ticker for allocations in model_portfolios.values() for ticker in allocations.keys()))
        
        # Build table data
        table_data = {'Portfolio': []}
        for ticker in all_tickers:
            table_data[ticker] = []
        
        for name, allocations in model_portfolios.items():
            indicator = " ⭐" if name == st.session_state.model_name else ""
            table_data['Portfolio'].append(f"{name}{indicator}")
            for ticker in all_tickers:
                weight = allocations.get(ticker, 0)
                table_data[ticker].append(f"{weight:.0%}" if weight > 0 else "-")
        
        df_models = pd.DataFrame(table_data)
        
        # Style the dataframe to make recommended portfolio bold
        def highlight_recommended(row):
            if '⭐' in str(row['Portfolio']):
                return ['font-weight: bold'] * len(row)
            else:
                return [''] * len(row)
        
        styled_df = df_models.style.apply(highlight_recommended, axis=1)
        
        st.dataframe(
            styled_df, 
            hide_index=True, 
            use_container_width=True,
            height=220
        )

    st.markdown("""
        <div style="margin-top: 2.5rem; padding: 1rem 0; border-bottom: 1px solid #e5e5e5;">
            <h2 style="font-size: 1.8rem; font-weight: 400; color: #1a1a1a; margin: 0;">
                🎯 Asset Allocation
            </h2>
            <p style="color: #6a6a6a; margin-top: 0.5rem; font-size: 0.95rem;">
                Compare your current portfolio allocation with the recommended model portfolio
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Define consistent colors for asset classes
    asset_class_colors = {
        'US Equities': '#3B82F6',           # Blue
        'International Equities': '#10B981', # Green
        'Core Fixed Income': '#F59E0B',      # Orange
        'Alternatives': '#8B5CF6'            # Purple
    }

    # Define the standard order for asset classes
    asset_class_order = ['US Equities', 'International Equities', 'Core Fixed Income', 'Alternatives']

    with col1:
        st.subheader("Your Portfolio")
        current_allocation = st.session_state.current_portfolio.asset_class_allocation

        # Create ordered allocation with all asset classes
        ordered_current = {ac: current_allocation.get(ac, 0) for ac in asset_class_order}
        
        # Filter out zero values for pie chart display
        display_values = [v for v in ordered_current.values() if v > 0]
        display_names = [k for k, v in ordered_current.items() if v > 0]

        if display_values:
            fig_current = px.pie(
                values=display_values,
                names=display_names,
                color=display_names,
                color_discrete_map=asset_class_colors,
                category_orders={'names': asset_class_order}
            )
            fig_current.update_traces(
                textposition='inside', 
                textinfo='percent+label', 
                textfont_size=12,
                textfont_color='white'
            )
            fig_current.update_layout(
                showlegend=False, 
                height=400,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='black')
            )
            st.plotly_chart(fig_current, use_container_width=True)

        # Display all asset classes in order, even if 0%
        for asset_class in asset_class_order:
            allocation = ordered_current[asset_class]
            st.write(f"**{asset_class}:** {allocation:.1%} (${allocation * total_value:,.0f})")

    with col2:
        st.subheader(f"{st.session_state.model_name} Portfolio")
        model_allocation = st.session_state.model_portfolio.asset_class_allocation

        # Create ordered allocation with all asset classes
        ordered_model = {ac: model_allocation.get(ac, 0) for ac in asset_class_order}
        
        # Filter out zero values for pie chart display
        display_values = [v for v in ordered_model.values() if v > 0]
        display_names = [k for k, v in ordered_model.items() if v > 0]

        if display_values:
            fig_model = px.pie(
                values=display_values,
                names=display_names,
                color=display_names,
                color_discrete_map=asset_class_colors,
                category_orders={'names': asset_class_order}
            )
            fig_model.update_traces(
                textposition='inside', 
                textinfo='percent+label', 
                textfont_size=12,
                textfont_color='white'
            )
            fig_model.update_layout(
                showlegend=False, 
                height=400,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color='black')
            )
            st.plotly_chart(fig_model, use_container_width=True)

        # Display all asset classes in order, even if 0%
        for asset_class in asset_class_order:
            allocation = ordered_model[asset_class]
            st.write(f"**{asset_class}:** {allocation:.1%} (${allocation * total_value:,.0f})")

    # Investment Details Table
    with st.expander("📋 View Investment Details"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Your Portfolio Holdings")
            current_details = st.session_state.current_portfolio.get_detailed_holdings()
            
            current_table_data = {
                'Ticker': [h['ticker'] for h in current_details],
                'Dollar Value': [h['dollar_value'] for h in current_details],
                'Yield': [h['yield'] * 100 for h in current_details],  # Convert to percentage
                'Expense Ratio': [h['expense_ratio'] * 100 for h in current_details],  # Convert to percentage
                'Category/Industry': [h['category'] for h in current_details]
            }
            
            df_current_details = pd.DataFrame(current_table_data)
            st.dataframe(
                df_current_details, 
                hide_index=True, 
                use_container_width=True,
                column_config={
                    'Dollar Value': st.column_config.NumberColumn('Dollar Value', format="$%.0f"),
                    'Yield': st.column_config.NumberColumn('Yield', format="%.2f%%"),
                    'Expense Ratio': st.column_config.NumberColumn('Expense Ratio', format="%.2f%%")
                }
            )
        
        with col2:
            st.markdown(f"#### {st.session_state.model_name} Portfolio Holdings")
            model_details = st.session_state.model_portfolio.get_detailed_holdings()
            
            model_table_data = {
                'Ticker': [h['ticker'] for h in model_details],
                'Dollar Value': [h['dollar_value'] for h in model_details],
                'Yield': [h['yield'] * 100 for h in model_details],  # Convert to percentage
                'Expense Ratio': [h['expense_ratio'] * 100 for h in model_details],  # Convert to percentage
                'Category/Industry': [h['category'] for h in model_details]
            }
            
            df_model_details = pd.DataFrame(model_table_data)
            st.dataframe(
                df_model_details, 
                hide_index=True, 
                use_container_width=True,
                column_config={
                    'Dollar Value': st.column_config.NumberColumn('Dollar Value', format="$%.0f"),
                    'Yield': st.column_config.NumberColumn('Yield', format="%.2f%%"),
                    'Expense Ratio': st.column_config.NumberColumn('Expense Ratio', format="%.2f%%")
                }
            )

    st.markdown("""
        <div style="margin-top: 2.5rem; padding: 1rem 0; border-bottom: 1px solid #e5e5e5;">
            <h2 style="font-size: 1.8rem; font-weight: 400; color: #1a1a1a; margin: 0;">
                📈 10-Year Forward Projections
            </h2>
            <p style="color: #6a6a6a; margin-top: 0.5rem; font-size: 0.95rem;">
                Projected growth comparison based on historical performance and fees
            </p>
        </div>
    """, unsafe_allow_html=True)

    current_proj_fees = st.session_state.current_projections_with_fees
    model_proj_fees = st.session_state.model_projections_with_fees

    # Create projection data with fees
    years = [0] + [p['year'] for p in current_proj_fees['yearly_projections']]
    current_values = [total_value] + [p['ending_value'] * total_value for p in current_proj_fees['yearly_projections']]
    model_values = [total_value] + [p['ending_value'] * total_value for p in model_proj_fees['yearly_projections']]

    fig_proj = go.Figure()

    fig_proj.add_trace(go.Scatter(
        x=years,
        y=current_values,
        mode='lines+markers',
        name='Your Portfolio',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=8)
    ))

    fig_proj.add_trace(go.Scatter(
        x=years,
        y=model_values,
        mode='lines+markers',
        name=f'{st.session_state.model_name} Model',
        line=dict(color='#06A77D', width=3),
        marker=dict(size=8)
    ))

    fig_proj.update_layout(
        title="Projected Portfolio Growth Over 10 Years (After Fees)",
        xaxis_title="Years",
        yaxis_title="Portfolio Value ($)",
        height=500,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    fig_proj.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5')
    fig_proj.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', tickformat='$,.0f')

    st.plotly_chart(fig_proj, use_container_width=True)

    # Show projection details
    col1, col2, col3 = st.columns(3)
    
    # Calculate net annual returns (after fees)
    current_total_fee_rate = st.session_state.current_portfolio.weighted_avg_er + st.session_state.current_portfolio.advisory_fee
    model_total_fee_rate = st.session_state.model_portfolio.weighted_avg_er + st.session_state.model_portfolio.advisory_fee
    
    current_net_return = current_proj_fees['weighted_annual_return'] - current_total_fee_rate
    model_net_return = model_proj_fees['weighted_annual_return'] - model_total_fee_rate
    
    with col1:
        st.metric(
            "Your Portfolio (10 yr)", 
            f"${current_values[-1]:,.0f}",
            f"{current_net_return:.2%} annual return (after fees)"
        )
    with col2:
        st.metric(
            f"{st.session_state.model_name} (10 yr)", 
            f"${model_values[-1]:,.0f}",
            f"{model_net_return:.2%} annual return (after fees)"
        )
    with col3:
        difference = model_values[-1] - current_values[-1]
        st.metric(
            "Potential Cumulative Difference", 
            f"${difference:,.0f}",
            f"{(difference/current_values[-1]*100):+.1f}%"
        )

    # Year-by-year projection tables
    with st.expander("📊 View Year-by-Year Projection Details"):
        st.markdown("#### Your Portfolio")
        
        # Build current portfolio table with years as columns
        current_table_data = {
            'Metric': ['Starting Value', 'Growth', 'Fees', 'Ending Value']
        }
        
        for i, p in enumerate(current_proj_fees['yearly_projections'], 1):
            current_table_data[f'Year {i}'] = [
                f"${p['starting_value'] * total_value:,.0f}",
                f"${p['growth'] * total_value:,.0f}",
                f"${p['fees'] * total_value:,.0f}",
                f"${p['ending_value'] * total_value:,.0f}"
            ]
        
        df_current = pd.DataFrame(current_table_data)
        st.dataframe(df_current, hide_index=True, use_container_width=True)
        
        st.markdown("---")
        st.markdown(f"#### {st.session_state.model_name} Portfolio")
        
        # Build model portfolio table with years as columns
        model_table_data = {
            'Metric': ['Starting Value', 'Growth', 'Fees', 'Ending Value']
        }
        
        for i, p in enumerate(model_proj_fees['yearly_projections'], 1):
            model_table_data[f'Year {i}'] = [
                f"${p['starting_value'] * total_value:,.0f}",
                f"${p['growth'] * total_value:,.0f}",
                f"${p['fees'] * total_value:,.0f}",
                f"${p['ending_value'] * total_value:,.0f}"
            ]
        
        df_model = pd.DataFrame(model_table_data)
        st.dataframe(df_model, hide_index=True, use_container_width=True)

    st.markdown("""
        <div style="margin-top: 2.5rem; padding: 1rem 0; border-bottom: 1px solid #e5e5e5;">
            <h2 style="font-size: 1.8rem; font-weight: 400; color: #1a1a1a; margin: 0;">
                💰 Projected Fees & Savings
            </h2>
            <p style="color: #6a6a6a; margin-top: 0.5rem; font-size: 0.95rem;">
                Compare projected annual and 10-year cumulative fees between your portfolio and the recommended model portfolio to determine potential savings 
            </p>
        </div>
    """, unsafe_allow_html=True)

    current_annual_fee = (st.session_state.current_portfolio.weighted_avg_er + st.session_state.current_portfolio.advisory_fee) * total_value
    model_annual_fee = (st.session_state.model_portfolio.weighted_avg_er + st.session_state.model_portfolio.advisory_fee) * total_value
    annual_savings = current_annual_fee - model_annual_fee

    # Calculate 10-year cumulative fees from projections
    current_cumulative_fees = st.session_state.current_projections_with_fees['total_fees'] * total_value
    model_cumulative_fees = st.session_state.model_projections_with_fees['total_fees'] * total_value
    cumulative_savings = current_cumulative_fees - model_cumulative_fees

    col1, col2 = st.columns(2)

    with col1:
        # Annual Fees Bar Chart
        fig_annual = go.Figure()

        fig_annual.add_trace(go.Bar(
            x=['Your Portfolio', st.session_state.model_name],
            y=[current_annual_fee, model_annual_fee],
            marker_color=['#2E86AB', '#06A77D'],
            text=[f'${current_annual_fee:,.0f}', f'${model_annual_fee:,.0f}'],
            textposition='outside',
            textfont=dict(size=14, color='black')
        ))

        fig_annual.update_layout(
            title="Annual Fees Comparison",
            yaxis_title="Annual Fees ($)",
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            font=dict(family="Arial, sans-serif", size=12)
        )

        fig_annual.update_yaxes(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='#E5E5E5', 
            tickformat='$,.0f',
            range=[0, max(current_annual_fee, model_annual_fee) * 1.15]
        )

        st.plotly_chart(fig_annual, use_container_width=True)

        st.metric("Annual Savings", f"${annual_savings:,.0f}", f"{(annual_savings/current_annual_fee*100):.1f}% reduction")

    with col2:
        # 10-Year Cumulative Fees Bar Chart
        fig_cumulative = go.Figure()

        fig_cumulative.add_trace(go.Bar(
            x=['Your Portfolio', st.session_state.model_name],
            y=[current_cumulative_fees, model_cumulative_fees],
            marker_color=['#2E86AB', '#06A77D'],
            text=[f'${current_cumulative_fees:,.0f}', f'${model_cumulative_fees:,.0f}'],
            textposition='outside',
            textfont=dict(size=14, color='black')
        ))

        fig_cumulative.update_layout(
            title="10-Year Cumulative Fees",
            yaxis_title="Total Fees ($)",
            height=400,
            plot_bgcolor='white',
            paper_bgcolor='white',
            showlegend=False,
            font=dict(family="Arial, sans-serif", size=12)
        )

        fig_cumulative.update_yaxes(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='#E5E5E5', 
            tickformat='$,.0f',
            range=[0, max(current_cumulative_fees, model_cumulative_fees) * 1.15]
        )

        st.plotly_chart(fig_cumulative, use_container_width=True)

        st.metric("10-Year Savings", f"${cumulative_savings:,.0f}", f"{(cumulative_savings/current_cumulative_fees*100):.1f}% reduction")

    # Fee breakdown details
    with st.expander("📊 Detailed Fee Breakdown"):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Your Portfolio")
            st.write(f"**Weighted Avg Expense Ratio:** {st.session_state.current_portfolio.weighted_avg_er:.3%}")
            st.write(f"**Advisory Fee:** {st.session_state.current_portfolio.advisory_fee:.3%}")
            st.write(f"**Total Annual Fee Rate:** {(st.session_state.current_portfolio.weighted_avg_er + st.session_state.current_portfolio.advisory_fee):.3%}")

        with col2:
            st.subheader(f"{st.session_state.model_name} Portfolio")
            st.write(f"**Weighted Avg Expense Ratio:** {st.session_state.model_portfolio.weighted_avg_er:.3%}")
            st.write(f"**Advisory Fee:** {st.session_state.model_portfolio.advisory_fee:.3%}")
            st.write(f"**Total Annual Fee Rate:** {(st.session_state.model_portfolio.weighted_avg_er + st.session_state.model_portfolio.advisory_fee):.3%}")

    st.markdown("""
        <div style="margin-top: 2.5rem; padding: 1rem 0; border-bottom: 1px solid #e5e5e5;">
            <h2 style="font-size: 1.8rem; font-weight: 400; color: #1a1a1a; margin: 0;">
                📊 Historical Performance
            </h2>
            <p style="color: #6a6a6a; margin-top: 0.5rem; font-size: 0.95rem;">
                Compare actual performance and risk statistics of your portfolio vs the recommended model portfolio over the past 10 years
            </p>
        </div>
    """, unsafe_allow_html=True)

    current_res = st.session_state.current_results
    model_res = st.session_state.model_results

    # Historical Growth Chart
    fig_hist = go.Figure()

    current_cumulative = current_res['cumulative_with_fees']
    model_cumulative = model_res['cumulative_with_fees']

    fig_hist.add_trace(go.Scatter(
        x=current_cumulative.index,
        y=current_cumulative * total_value,
        mode='lines',
        name='Your Portfolio',
        line=dict(color='#2E86AB', width=2)
    ))

    fig_hist.add_trace(go.Scatter(
        x=model_cumulative.index,
        y=model_cumulative * total_value,
        mode='lines',
        name=f'{st.session_state.model_name} Model',
        line=dict(color='#06A77D', width=2)
    ))

    fig_hist.update_layout(
        title="Historical Portfolio Growth",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        height=500,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12, color='black'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='black')),
        title_font=dict(color='black'),
        xaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black')),
        yaxis=dict(title_font=dict(color='black'), tickfont=dict(color='black'))
    )

    fig_hist.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5')
    fig_hist.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', tickformat='$,.0f')

    st.plotly_chart(fig_hist, use_container_width=True)

    # Performance Metrics Table
    metrics_data = {
        'Metric': ['Total Return', 'Annualized Return', 'Volatility', 'Sharpe Ratio', 'Max Drawdown'],
        'Your Portfolio': [
            f"{current_res['stats_with_fees']['Total Return']:.2%}",
            f"{current_res['stats_with_fees']['Annualized Return']:.2%}",
            f"{current_res['stats_with_fees']['Volatility']:.2%}",
            f"{current_res['stats_with_fees']['Sharpe Ratio']:.2f}",
            f"{current_res['stats_with_fees']['Max Drawdown']:.2%}"
        ],
        st.session_state.model_name: [
            f"{model_res['stats_with_fees']['Total Return']:.2%}",
            f"{model_res['stats_with_fees']['Annualized Return']:.2%}",
            f"{model_res['stats_with_fees']['Volatility']:.2%}",
            f"{model_res['stats_with_fees']['Sharpe Ratio']:.2f}",
            f"{model_res['stats_with_fees']['Max Drawdown']:.2%}"
        ]
    }

    df_metrics = pd.DataFrame(metrics_data)

    # Display the dataframe with Streamlit's native styling
    st.dataframe(
        df_metrics, 
        hide_index=True, 
        use_container_width=True,
        column_config={
            'Metric': st.column_config.TextColumn('Metric', width='medium'),
            'Your Portfolio': st.column_config.TextColumn('Your Portfolio', width='medium'),
            st.session_state.model_name: st.column_config.TextColumn(st.session_state.model_name, width='medium')
        }
    )

    st.caption(f"*Historical period: {current_res['actual_start_date']} to {current_res['actual_end_date']}*")

    # Footer
    st.markdown("""
        <div style="margin-top: 4rem; padding: 2rem 0 1rem 0; border-top: 2px solid #e5e5e5; text-align: center;">
            <p style="color: #6a6a6a; font-size: 0.85rem; margin-bottom: 0.5rem;">
                <strong>Disclaimer:</strong> This analysis is for informational purposes only and does not constitute financial advice.
            </p>
            <p style="color: #999; font-size: 0.8rem;">
                Past performance does not guarantee future results. Please consult with a qualified financial advisor before making investment decisions.
            </p>
        </div>
    """, unsafe_allow_html=True)