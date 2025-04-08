import streamlit as st
from streamlit import session_state as state
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go


def fetch_price_data(tickers, period="1y"):
    raw_data = yf.download(tickers, period=period, auto_adjust=False)

    if isinstance(raw_data.columns, pd.MultiIndex):
        # Multi-ticker format
        if "Adj Close" in raw_data:
            return raw_data["Adj Close"]
        elif "Close" in raw_data:
            return raw_data["Close"]
    else:
        # Single-ticker fallback
        if "Adj Close" in raw_data.columns:
            return raw_data[["Adj Close"]].rename(columns={"Adj Close": tickers[0]})
        elif "Close" in raw_data.columns:
            return raw_data[["Close"]].rename(columns={"Close": tickers[0]})

    raise KeyError("Neither 'Adj Close' nor 'Close' was found in the data.")

def risk_analysis(transactions):
    st.markdown("### ⚠️ Risk Analysis")

    if not transactions:
        st.info("Add transactions to view risk metrics.")
        return

    benchmark = "SPY"

    st.markdown("#### 📈 Enter a stock ticker to analyze:")
    selected_ticker = st.text_input("Ticker Symbol", placeholder="e.g. AAPL, TSLA, MSFT").upper()
    
    if not selected_ticker:
        st.stop()

    # Historical prices
    try:
        data = fetch_price_data([selected_ticker, benchmark], period="1y")
    except KeyError as e:
        st.error(str(e))
        return

    # Check if both tickers exist in columns
    if selected_ticker not in data.columns or benchmark not in data.columns:
        st.error(f"Missing data for {selected_ticker} or benchmark {benchmark}.")
        return
    
    # Calculate daily returns
    returns = data.pct_change().dropna()
    stock_returns = returns[selected_ticker]
    benchmark_returns = returns[benchmark]

    # Calculate Metrics
    volatility = np.std(stock_returns) * np.sqrt(252)
    sharpe_ratio = (np.mean(stock_returns) / np.std(stock_returns)) * np.sqrt(252)
    beta = np.cov(stock_returns, benchmark_returns)[0][1] / np.var(benchmark_returns)

    # Calculate drawdown
    cumulative = (1 + stock_returns).cumprod()
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    max_drawdown = drawdown.min()

    for key in ["vol_info", "sharpe_info", "beta_info", "drawdown_info"]:
        if key not in state:
            state[key] = False

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            "**📉 Volatility** <sup><span title='Volatility measures how much the stock price fluctuates. Higher volatility means more risk.' style='text-decoration:none; font-size:0.8em;'>ℹ️</span></sup>",
            unsafe_allow_html=True
        )
        st.metric(label=" ", value=f"{volatility:.2%}", label_visibility="collapsed")

    with col2:
        st.markdown(
            "**📊 Sharpe Ratio** <sup><span title='The Sharpe Ratio shows the risk-adjusted return. Higher is better.' style='text-decoration:none; font-size:0.8em;'>ℹ️</span></sup>",
            unsafe_allow_html=True
        )
        st.metric(label=" ", value=f"{sharpe_ratio:.2f}", label_visibility="collapsed")

    with col3:
        st.markdown(
            "**📐 Beta vs SPY** <sup><span title='Beta compares your stock’s volatility to the S&P 500. >1 means more volatile.' style='text-decoration:none; font-size:0.8em;'>ℹ️</span></sup>",
            unsafe_allow_html=True
        )
        st.metric(label=" ", value=f"{beta:.2f}", label_visibility="collapsed")

    with col4:
        st.markdown(
            "**📉 Max Drawdown** <sup><span title='Max drawdown is the biggest drop from peak to trough in value.' style='text-decoration:none; font-size:0.8em;'>ℹ️</span></sup>",
            unsafe_allow_html=True
        )
        st.metric(label=" ", value=f"{max_drawdown:.2%}", label_visibility="collapsed")

    # Plot drawdown
    st.markdown("#### 🔻 Drawdown Chart")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=drawdown.index, y=drawdown,
        mode="lines", fill='tozeroy',
        name="Drawdown", line=dict(color="red")
    ))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Drawdown",
        template="plotly_dark",
        height=400
    )
    st.plotly_chart(fig)