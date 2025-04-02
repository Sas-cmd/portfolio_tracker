import streamlit as st
import pandas as pd

def view_transactions(transactions):
    if transactions:
        df = pd.DataFrame(transactions)
        df["Date"] = pd.to_datetime(df["Date"])
        df.sort_values(by="Date", ascending=False, inplace=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No transactions yet. Add your first one above.")