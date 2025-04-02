import streamlit as st
from datetime import date
from data_manager import save_transactions


def add_transaction(transactions):
    st.markdown("### ➕ Add Transaction")

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
