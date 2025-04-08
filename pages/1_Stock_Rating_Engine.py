import streamlit as st
from modular_tabs.stock_rating.fundamentals import fundamental_score_ui

st.set_page_config(page_title="Stock Rating Engine", layout="wide")
st.title("🏅 Stock Rating Engine")

fundamental_score_ui()