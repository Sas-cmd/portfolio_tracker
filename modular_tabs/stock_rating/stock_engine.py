import yfinance as yf


import streamlit as st

def fundamental_score_ui():
    st.markdown("## 📊 Fundamental Score UI")
    st.info("This is the placeholder for fundamental score logic.")

# def fetch_fundamentals(ticker):
#     #"""Fetch fundamental metrics from yfinance."""
#     try:
#         stock = yf.Ticker(ticker)
#         info = stock.info

#         pe_ratio = info.get("trailingPE")
#         pb_ratio = info.get("priceToBook")
#         roe = info.get("returnOnEquity")
#         profit_margin = info.get("profitMargins")
#         debt_to_equity = info.get("debtToEquity")

#         return {
#             "P/E Ratio": pe_ratio,
#             "P/B Ratio": pb_ratio,
#             "ROE": roe,
#             "Profit Margin": profit_margin,
#             "Debt to Equity": debt_to_equity
#         }
#     except Exception as e:
#         print(f"Error fetching data for {ticker}: {e}")
#         return {}

# def score_value(pe, pb):
#     """Score value metrics (lower is better)."""
#     score = 0
#     if pe is not None:
#         if pe < 15:
#             score += 5
#         elif pe < 25:
#             score += 3
#         elif pe < 35:
#             score += 1
#     if pb is not None:
#         if pb < 1:
#             score += 5
#         elif pb < 3:
#             score += 3
#         elif pb < 5:
#             score += 1
#     return score

# def score_quality(roe, margin, debt):
#     """Score quality metrics (higher is better)."""
#     score = 0
#     if roe is not None:
#         if roe > 0.2:
#             score += 5
#         elif roe > 0.1:
#             score += 3
#         elif roe > 0.05:
#             score += 1
#     if margin is not None:
#         if margin > 0.2:
#             score += 5
#         elif margin > 0.1:
#             score += 3
#         elif margin > 0.05:
#             score += 1
#     if debt is not None:
#         if debt < 50:
#             score += 5
#         elif debt < 100:
#             score += 3
#         elif debt < 200:
#             score += 1
#     return score

# def overall_rating(value_score, quality_score):
#     """Compute final rating based on combined score."""
#     total = value_score + quality_score

#     if total >= 13:
#         return "Strong Buy", total
#     elif total >= 10:
#         return "Buy", total
#     elif total >= 6:
#         return "Hold", total
#     else:
#         return "Sell", total

# def rate_stock(ticker):
#     """Master function to rate stock."""
#     metrics = fetch_fundamentals(ticker)
#     if not metrics:
#         return "Data unavailable", {}

#     value_score = score_value(metrics["P/E Ratio"], metrics["P/B Ratio"])
#     quality_score = score_quality(metrics["ROE"], metrics["Profit Margin"], metrics["Debt to Equity"])
#     rating, total_score = overall_rating(value_score, quality_score)

#     return rating, {
#         "Value Score": value_score,
#         "Quality Score": quality_score,
#         "Total Score": total_score,
#         "Fundamentals": metrics
#     }
