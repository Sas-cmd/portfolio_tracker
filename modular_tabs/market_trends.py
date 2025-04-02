import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
    hist["Date"] = pd.to_datetime(hist["Date"]).dt.tz_localize(None)  # 👈 make dates tz-naive

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(hist["Date"], hist["Close"], label="Close Price", color="cyan")

    txn_for_ticker = [tx for tx in transactions if tx["Ticker"] == selected_ticker]
    if txn_for_ticker:
        start_date = hist["Date"].min()
        end_date = hist["Date"].max()

        buy_dates = []
        buy_prices = []

        for tx in txn_for_ticker:
            tx_date = pd.to_datetime(tx["Date"])
            tx_date = tx_date.tz_localize(None)  # 👈 make tx_date tz-naive
            if start_date <= tx_date <= end_date:
                matching_rows = hist[hist["Date"] == tx_date]
                if not matching_rows.empty:
                    buy_price = matching_rows["Close"].iloc[0]
                    buy_dates.append(tx_date)
                    buy_prices.append(buy_price)

        ax.scatter(buy_dates, buy_prices, marker='^', color='green', s=100, label='Buy')

    ax.set_title(f"{selected_ticker} - {selected_timeframe_label}", color="white")
    ax.set_xlabel("Date", color="white")
    ax.set_ylabel("Price ($)", color="white")
    ax.tick_params(colors="white")
    for spine in ["top", "right", "bottom", "left"]:
        ax.spines[spine].set_color("white")
    ax.legend()
    fig.patch.set_alpha(0)
    ax.set_facecolor('none')

    st.pyplot(fig)