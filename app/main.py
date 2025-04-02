import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_manager import load_transactions, save_transactions
from portfolio_metrics import calculate_performance
from plots import plot_allocation, plot_profit_loss
import sys
from pathlib import Path

from modular_tabs.add_transaction import add_transaction
from modular_tabs.delete_transactions import delete_transactions
from modular_tabs.import_export import import_export
from modular_tabs.market_trends import market_trends
from modular_tabs.view_transactions import view_transactions

# Set page config
st.set_page_config(page_title="Portfolio Tracker", layout="wide")
st.title("📈 Portfolio Tracker")

# Load existing transactions
transactions = load_transactions()

# -------------------------- Portfolio Summary -------------------------- #
if transactions:
    st.markdown("### 📊 Portfolio Summary")

    perf_df = calculate_performance(transactions)

    if not perf_df.empty:
        total_invested = perf_df["Invested ($)"].sum()
        total_current = perf_df["Current Value ($)"].sum()
        pl_amount = total_current - total_invested
        pl_percent = (pl_amount / total_invested) * 100 if total_invested else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Total Invested", f"${total_invested:,.2f}")
        col2.metric("📈 Market Value", f"${total_current:,.2f}")
        col3.metric("📊 Profit/Loss", f"${pl_amount:,.2f}")
        col4.metric("📉 Return", f"{pl_percent:.2f}%")

        st.subheader("💹 Live Portfolio Breakdown")
        st.dataframe(perf_df, hide_index=True)

        # Visual charts
        st.markdown("---")
        st.markdown("### 📊 Visual Portfolio Breakdown")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🥧 Portfolio Allocation")
            plot_allocation(perf_df)
        with col2:
            st.markdown("#### 📉 Profit / Loss by Ticker")
            plot_profit_loss(perf_df)

    else:
        st.warning("No valid performance data. Check your transactions.")
else:
    st.info("Add transactions to see your portfolio performance.")

# -------------------------- Tabs -------------------------- #
st.markdown("---")
st.subheader("📦 Transaction Management")

tabs = st.tabs([
    "➕ Add Transaction",
    "📋 View Transactions",
    "🗑️ Delete Transactions",
    "📁 Import / Export",
    "📊 Market Trends"
])

# Tab functionality
with tabs[0]:
    add_transaction(transactions)

with tabs[1]:
    view_transactions(transactions)

with tabs[2]:
    delete_transactions(transactions)

with tabs[3]:
    import_export(transactions)

with tabs[4]:
    market_trends(transactions)
