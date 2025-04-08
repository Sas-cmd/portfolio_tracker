import streamlit as st
from modular_tabs.stock_rating.value_metrics import rate_stock
from modular_tabs.stock_rating.score_utils import score_to_badge

def fundamental_score_ui():
    st.markdown("### 🧮 Fundamental Stock Rating")

    ticker = st.text_input("Enter a stock ticker:", "AAPL")

    if ticker:
        rating, results = rate_stock(ticker)

        st.markdown(f"### ✅ Overall Rating: **{rating}**")

        col1, col2, col3 = st.columns(3)
        col1.metric("📊 Total Score", results["Total Score"])
        col2.metric("💸 Value Score", results["Value Score"])
        col3.metric("🏢 Quality Score", results["Quality Score"])

        st.markdown("---")

        fundamentals = results["Fundamentals"]

        # Keys grouped by metric type
        value_keys = [
            "P/E Ratio", "P/B Ratio", "PEG Ratio", "Price to FCF", "EV/EBITDA", "Earnings Yield"
        ]
        quality_keys = [
            "ROE", "ROA", "Operating Margin", "Gross Margin", "Debt to Equity", "Interest Coverage Ratio"
        ]

        # Value Metrics Section
        st.markdown("### 🧾 Value Metrics")
        cols_v = st.columns(3)
        for i, key in enumerate(value_keys):
            value = fundamentals.get(key)
            score = fundamentals.get(f"{key} Score")

            with cols_v[i % 3]:
                value_str = round(value, 4) if isinstance(value, (int, float)) else "N/A"
                # If score exists, show it with badge
                if score is not None:
                    badge = score_to_badge(score)
                    score_str = f"&nbsp;&nbsp;{badge} ({score})"
                else:
                    score_str = ""

                st.markdown(f"**{key}:** {value_str} {score_str}", unsafe_allow_html=True)


        # Quality Metrics Section
        st.markdown("### 🧰 Quality Metrics")
        quality_items = [(k, fundamentals.get(k)) for k in quality_keys if k in fundamentals]
        cols_q = st.columns(3)

        for i, (key, value) in enumerate(quality_items):
            with cols_q[i % 3]:
                val_str = round(value, 4) if isinstance(value, (int, float)) else "N/A"
                
                # Retrieve associated score
                score_key = f"{key} Score"
                score = fundamentals.get(score_key)

                if score is not None:
                    badge = score_to_badge(score)
                    score_str = f"&nbsp;&nbsp;{badge} ({score})"
                else:
                    score_str = ""

                st.markdown(f"**{key}:** {val_str} {score_str}", unsafe_allow_html=True)