import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime

def market_trends(transactions):
    st.markdown("### 📊 Market Trends")

    if not transactions:
        st.info("No transactions found. Add some before viewing Market Trends.")
        return

    ticker_list = sorted(set(txn["Ticker"] for txn in transactions))
    selected_ticker = st.selectbox("Select a Ticker", options=ticker_list)

    timeframes = {
        "1 Day": "1d",
        "1 Week": "7d",
        "1 Month": "1mo",
        "1 Year": "1y",
        "5 Years": "5y",
        "YTD": None,
        "Max": "max"
    }

    selected_timeframe_label = st.selectbox("Select Timeframe", options=list(timeframes.keys()), index=3)

    if selected_timeframe_label == "YTD":
        start = datetime(datetime.now().year, 1, 1)
        hist = yf.download(selected_ticker, start=start)
    else:
        period = timeframes[selected_timeframe_label]
        hist = yf.Ticker(selected_ticker).history(period=period)

    if hist.empty:
        st.warning(f"No data returned for {selected_ticker} in timeframe: {selected_timeframe_label}")
        return

    hist.reset_index(inplace=True)
    hist["Date"] = pd.to_datetime(hist["Date"]).dt.tz_localize(None)

    fig = go.Figure()

    # Stock Price Line
    fig.add_trace(go.Scatter(
        x=hist["Date"],
        y=hist["Close"],
        mode="lines",
        name="Price",
        line=dict(color="#00FFFF", width=2),  # cyan-ish line
        hovertemplate="Date: %{x|%Y-%m-%d}<br>Price: $%{y:.2f}<extra></extra>"
    ))

    # Buy Markers
    txn_for_ticker = [tx for tx in transactions if tx["Ticker"] == selected_ticker]
    buy_dates = []
    buy_prices = []

    start_date = hist["Date"].min()
    end_date = hist["Date"].max()

    for tx in txn_for_ticker:
        tx_date = pd.to_datetime(tx["Date"])
        if start_date <= tx_date <= end_date:
            match = hist[hist["Date"] == tx_date]
            if not match.empty:
                buy_dates.append(tx_date)
                buy_prices.append(match["Close"].iloc[0])

    if buy_dates:
        fig.add_trace(go.Scatter(
            x=buy_dates,
            y=buy_prices,
            mode="markers",
            name="Buy",
            marker=dict(
                symbol="diamond",
                color="lime",
                size=12,
                line=dict(width=1, color="white")
            ),
            hovertemplate="Buy Date: %{x|%Y-%m-%d}<br>Price: $%{y:.2f}<extra></extra>",
        ))

    # Layout styling for dark mode
    fig.update_layout(
        title=f"{selected_ticker} - {selected_timeframe_label}",
        xaxis_title="Date",
        yaxis_title="Price ($)",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        hovermode="x unified",
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )
    )

    st.plotly_chart(fig, use_container_width=True)