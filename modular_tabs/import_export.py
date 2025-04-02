import streamlit as st
import pandas as pd
import json
from data_manager import save_transactions

def import_export(transactions):
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

    if st.button("Export", key="export_button"):
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
                json_data = json.dumps(transactions, indent=2).encode("utf-8")
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name="portfolio_transactions.json",
                    mime="application/json"
                )
        else:
            st.warning("No transactions available to export.")