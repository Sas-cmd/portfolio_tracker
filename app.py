import streamlit as st
import pandas as pd
import json
from datetime import date
from pathlib import Path
import yfinance as yf
import matplotlib.pyplot as plt

# Store transactions
DATA_FILE = Path("data/transactions.json")

# Load existing transactions
def load_transactions():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save transactions to file
def save_transactions(transactions):
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=2)

# Streamlit 
st.set_page_config(page_title="Portfolio Tracker", layout="wide")
st.title("📈 Portfolio Tracker")

# Load current transactions
transactions = load_transactions()

#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Portfolio Summary 
if transactions:
    st.markdown("### 📊 Portfolio Summary")
    total_invested = 0
    total_current = 0
    performance_data = []

    tickers = list(set([txn["Ticker"] for txn in transactions]))
    prices = {}
    for ticker in tickers:
        try:
            tkr = yf.Ticker(ticker)
            hist = tkr.history(period="1d")
            if not hist.empty:
                prices[ticker] = hist["Close"].iloc[-1]
            else:
                st.warning(f"No data returned for {ticker}.")
        except Exception as e:
            st.warning(f"Couldn't fetch price for {ticker}: {e}")

    for txn in transactions:
        ticker = txn["Ticker"]
        shares = txn["Shares"]
        invested = shares * txn["Price Paid"]
        current_price = prices.get(ticker, txn["Price Paid"])
        current_value = shares * current_price
        profit_loss = current_value - invested

        total_invested += invested
        total_current += current_value

        performance_data.append({
            "Stock": txn["Stock"],
            "Ticker": ticker,
            "Shares": shares,
            "Avg Cost": txn["Price Paid"],
            "Live Price": round(current_price, 2),
            "Invested ($)": round(invested, 2),
            "Current Value ($)": round(current_value, 2),
            "P/L ($)": round(profit_loss, 2),
            "P/L (%)": round((profit_loss / invested) * 100, 2) if invested > 0 else 0
        })

    perf_df = pd.DataFrame(performance_data)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Invested", f"${total_invested:,.2f}")
    col2.metric("📈 Market Value", f"${total_current:,.2f}")
    col3.metric("📊 Profit/Loss", f"${(total_current - total_invested):,.2f}")
    col4.metric("📉 Return", f"{((total_current - total_invested) / total_invested) * 100:.2f}%")

    st.subheader("💹 Live Portfolio Breakdown")
    st.dataframe(perf_df, hide_index=True)
else:
    st.info("Add transactions to see your portfolio performance.")

#--------------------------------------------------------------------#

#--------------------------------------------------------------------#

# PIE CHART: Allocation
if transactions:
    st.markdown("---")
    st.markdown("### 📊 Visual Portfolio Breakdown")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🥧 Portfolio Allocation")
        alloc_df = perf_df[["Ticker", "Current Value ($)"]].groupby("Ticker").sum()
        fig1, ax1 = plt.subplots(figsize=(4, 4), facecolor='none')
        wedges, texts, autotexts = ax1.pie(
            alloc_df["Current Value ($)"],
            labels=alloc_df.index,
            autopct="%1.1f%%",
            startangle=90,
            wedgeprops=dict(width=0.4)
        )
        for text in texts + autotexts:
            text.set_color("white")
        ax1.axis("equal")
        fig1.patch.set_alpha(0)
        st.pyplot(fig1)

    with col2:
        st.markdown("#### 📉 Profit / Loss by Ticker")
        fig2, ax2 = plt.subplots(figsize=(5, 4), facecolor='none')
        colors = ['green' if val >= 0 else 'red' for val in perf_df["P/L ($)"]]
        bars = ax2.bar(perf_df["Ticker"], perf_df["P/L ($)"], color=colors)

        ax2.set_facecolor('none')
        fig2.patch.set_alpha(0)
        ax2.set_ylabel("P/L ($)", color="white")
        ax2.set_title("Profit/Loss per Stock", color="white")
        ax2.tick_params(colors="white", rotation=45)

        for spine in ["top", "right"]:
            ax2.spines[spine].set_visible(False)
        for spine in ["bottom", "left"]:
            ax2.spines[spine].set_color("white")

        for i, bar in enumerate(bars):
            value = perf_df["P/L ($)"].iloc[i]
            pct = perf_df["P/L (%)"].iloc[i]
            ax2.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + (0.01 if value >= 0 else -0.05),
                f"${value:.2f}\n({pct:.2f}%)",
                ha='center',
                va='bottom' if value >= 0 else 'top',
                color='white',
                fontsize=8
            )

        fig2.tight_layout()
        st.pyplot(fig2)

#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Making all of these into TABS
# Transactions Tab
st.markdown("---")
st.subheader("📦 Transaction Management")
tabs = st.tabs(["➕ Add Transaction", "📋 View Transactions", "🗑️ Delete Transactions"])

# Tab 1: Add Transaction
with tabs[0]:
    with st.form("add_transaction_form"):
        stock = st.text_input("Stock Name", placeholder="")
        ticker = st.text_input("Ticker Symbol", placeholder="e.g. VTS or IVV")
        shares = st.number_input("Number of Shares", min_value=0.01, step=0.01, format="%.2f")
        price = st.number_input("Price Paid per Share ($)", min_value=0.01, step=0.01, format="%.2f")
        purchase_date = st.date_input("Date of Purchase", value=date.today())
        submit = st.form_submit_button("Add Transaction")

    if submit:
        new_txn = {
            "Stock": stock,
            "Ticker": ticker.upper(),
            "Shares": float(shares),
            "Price Paid": float(price),
            "Date": str(purchase_date)
        }
        transactions.append(new_txn)
        save_transactions(transactions)
        st.success("Transaction added!")
        st.rerun()

#--------------------------------------------------------------------#

#--------------------------------------------------------------------#

# Tab 2: View Transactions
with tabs[1]:
    if transactions:
        df = pd.DataFrame(transactions)
        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values(by="Date", ascending=False, inplace=True)
        st.dataframe(df)
    else:
        st.info("No transactions yet. Add your first one above.")
#--------------------------------------------------------------------#

#--------------------------------------------------------------------#
# Tab 3: Delete Transactions
with tabs[2]:
    if transactions:
        for i, txn in enumerate(transactions):
            col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 2, 2, 2, 1])
            col1.write(txn["Stock"])
            col2.write(txn["Ticker"])
            col3.write(f"{txn['Shares']} @ ${txn['Price Paid']}")
            col4.write(txn["Date"])
            if col5.button("Delete", key=f"delete_{i}"):
                transactions.pop(i)
                save_transactions(transactions)
                st.success("Transaction deleted.")
                st.rerun()
    else:
        st.info("No transactions available to delete.")

#--------------------------------------------------------------------#


