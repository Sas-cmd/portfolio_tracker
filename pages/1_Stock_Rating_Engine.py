import streamlit as st

st.set_page_config(page_title="Stock Rating Engine", layout="wide")
st.title("🏅 Stock Rating Engine")

try:
    from modular_tabs.stock_rating.stock_engine import fundamental_score_ui
    fundamental_score_ui()
except ModuleNotFoundError:
    st.warning("Fundamental scoring module not found yet. Coming soon!")
except ImportError:
    st.warning("Function 'fundamental_score_ui()' missing or not defined yet.")