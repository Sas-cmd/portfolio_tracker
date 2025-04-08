import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from data_manager import save_transactions

def delete_transactions(transactions):
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