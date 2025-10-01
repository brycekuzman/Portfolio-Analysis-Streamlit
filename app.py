import streamlit as st
import pandas as pd
import numpy as np
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
    initial_sidebar_state="collapsed"
)

# Custom CSS for clean, minimalist design
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    h1 {
        font-weight: 300;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    h2 {
        font-weight: 300;
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #333;
    }
    h3 {
        font-weight: 400;
        font-size: 1.3rem;
        margin-top: 1.5rem;
        color: #555;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 500;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {"VOO": 20000, "VXUS": 10000, "BND": 10000}
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

# Header
st.title("Portfolio Analysis Dashboard")
st.markdown("Compare your investment portfolio against optimized model portfolios")

# Portfolio Input Section
st.markdown("---")
st.header("Your Portfolio")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Holdings")
    
    # Display current holdings
    for i, (ticker, amount) in enumerate(list(st.session_state.portfolio.items())):
        cols = st.columns([2, 3, 1])
        with cols[0]:
            new_ticker = st.text_input(f"Ticker", value=ticker, key=f"ticker_{i}", label_visibility="collapsed")
        with cols[1]:
            new_amount = st.number_input(f"Amount", value=float(amount), min_value=0.0, step=1000.0, key=f"amount_{i}", label_visibility="collapsed", format="%.2f")
        with cols[2]:
            if st.button("🗑️", key=f"remove_{i}"):
                del st.session_state.portfolio[ticker]
                st.rerun()
        
        # Update portfolio
        if new_ticker != ticker:
            del st.session_state.portfolio[ticker]
            st.session_state.portfolio[new_ticker.upper()] = new_amount
        else:
            st.session_state.portfolio[ticker] = new_amount
    
    # Add new holding
    col_add1, col_add2 = st.columns([1, 3])
    with col_add1:
        if st.button("➕ Add Holding", use_container_width=True):
            st.session_state.portfolio[f"NEW{len(st.session_state.portfolio)}"] = 1000.0
            st.rerun()

with col2:
    st.subheader("Settings")
    advisory_fee = st.number_input(
        "Advisory Fee (%)", 
        min_value=0.0, 
        max_value=5.0, 
        value=1.0, 
        step=0.05,
        help="Your current advisory fee percentage"
    ) / 100
    
    total_value = sum(st.session_state.portfolio.values())
    st.metric("Total Portfolio Value", f"${total_value:,.0f}")

# Analyze Button
st.markdown("")
if st.button("🔍 Analyze Portfolio", use_container_width=False, type="primary"):
    with st.spinner("Analyzing your portfolio..."):
        try:
            # Create current portfolio
            current_portfolio = Portfolio(st.session_state.portfolio, "Current", advisory_fee)
            
            # Find best matching model
            best_match, similarity = find_best_matching_model(current_portfolio.asset_class_allocation)
            model_name, model_allocations = best_match
            
            # Create model portfolio
            model_portfolio_dollars = {ticker: total_value * weight for ticker, weight in model_allocations.items()}
            model_portfolio = Portfolio(model_portfolio_dollars, model_name, model_fee)
            
            # Historical analysis
            start_date, end_date = "2015-09-30", "2025-08-29"
            current_results = current_portfolio.analyze_historical_performance(start_date, end_date)
            model_results = model_portfolio.analyze_historical_performance(current_results['actual_start_date'], end_date)
            
            # Future projections
            current_projections = current_portfolio.project_future_returns(10)
            model_projections = model_portfolio.project_future_returns(10)
            
            # Store in session state
            st.session_state.current_portfolio = current_portfolio
            st.session_state.model_portfolio = model_portfolio
            st.session_state.model_name = model_name
            st.session_state.similarity = similarity
            st.session_state.current_results = current_results
            st.session_state.model_results = model_results
            st.session_state.current_projections = current_projections
            st.session_state.model_projections = model_projections
            st.session_state.analyzed = True
            
            st.success(f"Analysis complete! Best match: **{model_name}** Portfolio ({similarity:.1%} similarity)")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            st.session_state.analyzed = False

# Results Section
if st.session_state.analyzed:
    st.markdown("---")
    
    # Model Portfolio Info
    st.header(f"Recommended: {st.session_state.model_name} Portfolio")
    st.markdown(f"*Asset allocation similarity: {st.session_state.similarity:.1%}*")
    
    # Display model allocations
    cols = st.columns(5)
    for i, (ticker, weight) in enumerate(st.session_state.model_portfolio.portfolio_weights.items()):
        with cols[i % 5]:
            st.metric(ticker, f"{weight:.1%}")
    
    st.markdown("---")
    
    # Forward Projections Chart
    st.header("📈 10-Year Forward Projections")
    
    current_proj = st.session_state.current_projections
    model_proj = st.session_state.model_projections
    
    # Create projection data
    years = [0] + [p['year'] for p in current_proj['yearly_projections']]
    current_values = [total_value] + [p['portfolio_value'] * total_value for p in current_proj['yearly_projections']]
    model_values = [total_value] + [p['portfolio_value'] * total_value for p in model_proj['yearly_projections']]
    
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
        title="Projected Portfolio Growth Over 10 Years",
        xaxis_title="Years",
        yaxis_title="Portfolio Value ($)",
        height=500,
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial, sans-serif", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig_proj.update_xaxis(showgrid=True, gridwidth=1, gridcolor='#E5E5E5')
    fig_proj.update_yaxis(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', tickformat='$,.0f')
    
    st.plotly_chart(fig_proj, use_container_width=True)
    
    # Show projection details
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Your Portfolio (10 yr)", 
            f"${current_values[-1]:,.0f}",
            f"{current_proj['weighted_annual_return']:.2%} annual"
        )
    with col2:
        st.metric(
            f"{st.session_state.model_name} (10 yr)", 
            f"${model_values[-1]:,.0f}",
            f"{model_proj['weighted_annual_return']:.2%} annual"
        )
    with col3:
        difference = model_values[-1] - current_values[-1]
        st.metric(
            "Potential Difference", 
            f"${difference:,.0f}",
            f"{(difference/current_values[-1]*100):+.1f}%"
        )
    
    st.markdown("---")
    
    # Fee Comparison
    st.header("💰 Fee Comparison & Savings")
    
    current_annual_fee = (st.session_state.current_portfolio.weighted_avg_er + st.session_state.current_portfolio.advisory_fee) * total_value
    model_annual_fee = (st.session_state.model_portfolio.weighted_avg_er + st.session_state.model_portfolio.advisory_fee) * total_value
    annual_savings = current_annual_fee - model_annual_fee
    
    # Calculate 10-year cumulative fees
    current_cumulative_fees = current_annual_fee * 10
    model_cumulative_fees = model_annual_fee * 10
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
        
        fig_annual.update_yaxis(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', tickformat='$,.0f')
        
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
        
        fig_cumulative.update_yaxis(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', tickformat='$,.0f')
        
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
    
    st.markdown("---")
    
    # Historical Performance
    st.header("📊 Historical Performance")
    
    current_res = st.session_state.current_results
    model_res = st.session_state.model_results
    
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
    st.dataframe(df_metrics, hide_index=True, use_container_width=True)
    
    st.caption(f"*Historical period: {current_res['actual_start_date']} to {current_res['actual_end_date']}*")
    
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
        font=dict(family="Arial, sans-serif", size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig_hist.update_xaxis(showgrid=True, gridwidth=1, gridcolor='#E5E5E5')
    fig_hist.update_yaxis(showgrid=True, gridwidth=1, gridcolor='#E5E5E5', tickformat='$,.0f')
    
    st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown("---")
    
    # Asset Allocation
    st.header("🎯 Asset Allocation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Your Portfolio")
        current_allocation = st.session_state.current_portfolio.asset_class_allocation
        
        fig_current = px.pie(
            values=list(current_allocation.values()),
            names=list(current_allocation.keys()),
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig_current.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12)
        fig_current.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_current, use_container_width=True)
        
        for asset_class, allocation in current_allocation.items():
            st.write(f"**{asset_class}:** {allocation:.1%} (${allocation * total_value:,.0f})")
    
    with col2:
        st.subheader(f"{st.session_state.model_name} Portfolio")
        model_allocation = st.session_state.model_portfolio.asset_class_allocation
        
        fig_model = px.pie(
            values=list(model_allocation.values()),
            names=list(model_allocation.keys()),
            color_discrete_sequence=px.colors.sequential.Greens_r
        )
        fig_model.update_traces(textposition='inside', textinfo='percent+label', textfont_size=12)
        fig_model.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig_model, use_container_width=True)
        
        for asset_class, allocation in model_allocation.items():
            st.write(f"**{asset_class}:** {allocation:.1%} (${allocation * total_value:,.0f})")
    
    st.markdown("---")
    
    # All Model Portfolios Reference
    with st.expander("📚 View All Model Portfolios"):
        st.subheader("Available Model Portfolios")
        
        for name, allocations in model_portfolios.items():
            indicator = " ⭐ (Recommended)" if name == st.session_state.model_name else ""
            st.markdown(f"### {name}{indicator}")
            
            cols = st.columns(len(allocations))
            for i, (ticker, weight) in enumerate(allocations.items()):
                with cols[i]:
                    st.metric(ticker, f"{weight:.0%}")
            
            st.markdown("")
