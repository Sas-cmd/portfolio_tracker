import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, datetime
import yfinance as yf

from data_manager import load_transactions, save_transactions
from portfolio_metrics import calculate_performance
from plots import plot_allocation, plot_profit_loss

# Set Streamlit page config
st.set_page_config(page_title="Portfolio Tracker", layout="wide")
st.title("📈 Portfolio Tracker")

transactions = load_transactions()

# ------------------------- Portfolio Summary -------------------------
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
    else:
        st.warning("No valid performance data. Check your transactions.")
else:
    st.info("Add transactions to see your portfolio performance.")

# ------------------------- Portfolio Plots -------------------------
if transactions:
    st.markdown("---")
    st.markdown("### 📊 Visual Portfolio Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🥧 Portfolio Allocation")
        plot_allocation(perf_df)
    with col2:
        st.markdown("#### 📉 Profit / Loss by Ticker")
        plot_profit_loss(perf_df)

# ------------------------- Tabs -------------------------
st.markdown("---")
st.subheader("📦 Transaction Management")
tabs = st.tabs([
    "➕ Add Transaction",
    "📋 View Transactions",
    "🗑️ Delete Transactions",
    "📁 Import / Export",
    "📊 Market Trends"
])

# ------------------------- Tab 1: Add -------------------------
with tabs[0]:
    with st.form("add_transaction_form"):
        stock = st.text_input("Stock Name")
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
        st.experimental_rerun()

# ------------------------- Tab 2: View -------------------------
with tabs[1]:
    if transactions:
        df = pd.DataFrame(transactions)
        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values(by="Date", ascending=False, inplace=True)
        st.dataframe(df)
    else:
        st.info("No transactions yet. Add your first one above.")

# ------------------------- Tab 3: Delete -------------------------
with tabs[2]:
    if transactions:
        for i, txn in enumerate(transactions):
            col1, col2, col3, col4, col5, col6 = st.columns([3, 2, 3, 3, 2, 1])
            col1.write(txn["Stock"])
            col2.write(txn["Ticker"])
            col3.write(f"{txn['Shares']} @ ${txn['Price Paid']}")
            col4.write(txn["Date"])
            if col5.button("Delete", key=f"delete_{i}"):
                transactions.pop(i)
                save_transactions(transactions)
                st.success("Transaction deleted.")
                st.experimental_rerun()
    else:
        st.info("No transactions available to delete.")

# ------------------------- Tab 4: Import/Export -------------------------
with tabs[3]:
    st.markdown("### 📥 Import Transactions")
    uploaded_file = st.file_uploader("Upload CSV or JSON File", type=["csv", "json"], key="import_uploader")

    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                imported_df = pd.read_csv(uploaded_file)
            else:
                imported_df = pd.read_json(uploaded_file)

            required_cols = {"Stock", "Ticker", "Shares", "Price Paid", "Date"}
            if not required_cols.issubset(imported_df.columns):
                st.error("Uploaded file is missing required columns.")
            else:
                imported = imported_df.to_dict(orient="records")
                transactions.extend(imported)
                save_transactions(transactions)
                st.success(f"Successfully imported {len(imported)} transactions.")
                st.experimental_rerun()

        except Exception as e:
            st.error(f"Error importing file: {e}")

    st.markdown("---")
    st.markdown("### 📤 Export Transactions")

    export_format = st.selectbox("Select Export Format", ["CSV", "JSON"], key="export_format_selectbox")
    if st.button("Export", key="export_button"):
        if transactions:
            df_export = pd.DataFrame(transactions)
            if export_format == "CSV":
                csv_data = df_export.to_csv(index=False).encode("utf-8")
                st.download_button("📥 Download CSV", data=csv_data, file_name="portfolio_transactions.csv", mime="text/csv")
            else:
                json_data = df_export.to_json(orient="records", indent=2).encode("utf-8")
                st.download_button("📥 Download JSON", data=json_data, file_name="portfolio_transactions.json", mime="application/json")
        else:
            st.warning("No transactions available to export.")

# ------------------------- Tab 5: Market Trends -------------------------
with tabs[4]:
    st.markdown("### 📊 Market Trends")

    if not transactions:
        st.info("No transactions found. Add some before viewing Market Trends.")
    else:
        ticker_list = sorted(set(txn["Ticker"] for txn in transactions))
        selected_ticker = st.selectbox("Select a Ticker", options=ticker_list)

        timeframes = {
            "1 Day": "1d",
            "1 Week": "7d",
            "1 Month": "1mo",
            "1 Year": "1y",
            "5 Years": "5y",
            "Max": "max",
            "YTD": "ytd"
        }

        selected_timeframe_label = st.selectbox(
            "Select Timeframe",
            options=list(timeframes.keys()),
            index=3
        )

        ticker_data = yf.Ticker(selected_ticker)

        if selected_timeframe_label == "YTD":
            start_of_year = pd.Timestamp(datetime(date.today().year, 1, 1))
            end_of_day = pd.Timestamp(date.today())
            hist = ticker_data.history(start=start_of_year, end=end_of_day)
        else:
            period = timeframes[selected_timeframe_label]
            hist = ticker_data.history(period=period)

        if hist.empty:
            st.warning(f"No data returned for {selected_ticker} in timeframe: {selected_timeframe_label}")
        else:
            fig, ax = plt.subplots(figsize=(10, 4))
            hist.reset_index(inplace=True)
            ax.plot(hist["Date"], hist["Close"], label="Close Price", color="cyan")

            txn_for_ticker = [tx for tx in transactions if tx["Ticker"] == selected_ticker]
            if txn_for_ticker:
                start_date = hist["Date"].min().tz_localize(None)
                end_date = hist["Date"].max().tz_localize(None)

                buy_dates = []
                buy_prices = []

                for tx in txn_for_ticker:
                    tx_date = pd.to_datetime(tx["Date"])
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

