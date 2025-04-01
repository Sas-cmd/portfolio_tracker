import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# Import our custom modules
from data_manager import load_transactions, save_transactions
from portfolio_metrics import calculate_performance
from plots import plot_allocation, plot_profit_loss

# Set Streamlit page config
st.set_page_config(page_title="Portfolio Tracker", layout="wide")
st.title("📈 Portfolio Tracker")

# Load existing transactions
transactions = load_transactions()

# Portfolio Summary
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

# Portfolio Plots
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

# Transaction Management
st.markdown("---")
st.subheader("📦 Transaction Management")
tabs = st.tabs([
    "➕ Add Transaction",
    "📋 View Transactions",
    "🗑️ Delete Transactions",
    "📁 Import / Export"
])

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
        st.experimental_rerun()

# Tab 2: View Transactions
with tabs[1]:
    if transactions:
        df = pd.DataFrame(transactions)
        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values(by="Date", ascending=False, inplace=True)
        st.dataframe(df)
    else:
        st.info("No transactions yet. Add your first one above.")

# Tab 3: Delete Transactions
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

# Tab 4: Import / Export
with tabs[3]:
    st.markdown("### 📥 Import Transactions")
    uploaded_file = st.file_uploader(
        "Upload CSV or JSON File",
        type=["csv", "json"],
        key="import_file_uploader"
    )

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

    export_format = st.selectbox(
        "Select Export Format",
        ["CSV", "JSON"],
        key="export_format_selectbox"
    )

    if st.button("Export"):
        if transactions:
            df_export = pd.DataFrame(transactions)

            if export_format == "CSV":
                csv_data = df_export.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name="portfolio_transactions.csv",
                    mime="text/csv"
                )

            elif export_format == "JSON":
                json_data = df_export.to_json(orient="records", indent=2).encode("utf-8")
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name="portfolio_transactions.json",
                    mime="application/json"
                )
        else:
            st.warning("No transactions available to export.")
