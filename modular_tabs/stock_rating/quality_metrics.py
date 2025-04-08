import yfinance as yf
import pandas as pd 
from modular_tabs.stock_rating.data_fetcher import fetch_all_data

def fetch_quality_metrics(ticker):
    try:
        data = fetch_all_data(ticker)
        info = data.get("info", {})
        financials = data.get("financials", None)

        roe = info.get("returnOnEquity")
        roa = info.get("returnOnAssets")
        op_margin = info.get("operatingMargins")
        gross_margin = info.get("grossMargins")
        debt_to_equity = info.get("debtToEquity")

        # Fallback for missing info fields
        if not all([roe, roa, op_margin, gross_margin, debt_to_equity]):
            from modular_tabs.stock_rating.data_fetcher import fetch_from_fmp
            fmp_info = fetch_from_fmp(ticker).get("info", {})
            roe = roe or fmp_info.get("roe")
            roa = roa or fmp_info.get("roa")
            op_margin = op_margin or fmp_info.get("operatingMargin")
            gross_margin = gross_margin or fmp_info.get("grossMargin")
            debt_to_equity = debt_to_equity or fmp_info.get("debtToEquity")

        # Interest Coverage Ratio from Yahoo (if possible)
        interest_coverage = None
        if isinstance(financials, pd.DataFrame):
            try:
                ebit = financials.loc["EBIT"].dropna().iloc[0]
                interest_expense = financials.loc["Interest Expense"].dropna().iloc[0]
                if interest_expense != 0:
                    interest_coverage = abs(ebit / interest_expense)
            except:
                pass

        return {
            "ROE": roe,
            "ROA": roa,
            "Operating Margin": op_margin,
            "Gross Margin": gross_margin,
            "Debt to Equity": debt_to_equity,
            "Interest Coverage Ratio": interest_coverage
        }

    except Exception as e:
        print(f"❌ Error fetching quality metrics for {ticker}: {e}")
        return {}
    
    
def score_quality(roe, roa, op_margin, gross_margin, debt, interest_coverage):
    score = {}

    # ROE
    if roe is not None:
        if roe > 0.25:
            score["ROE Score"] = 5
        elif roe > 0.2:
            score["ROE Score"] = 4
        elif roe > 0.1:
            score["ROE Score"] = 3
        elif roe > 0.05:
            score["ROE Score"] = 2
        elif roe > 0:
            score["ROE Score"] = 1
        else:
            score["ROE Score"] = 0

    # ROA
    if roa is not None:
        if roa > 0.15:
            score["ROA Score"] = 5
        elif roa > 0.1:
            score["ROA Score"] = 4
        elif roa > 0.05:
            score["ROA Score"] = 3
        elif roa > 0.02:
            score["ROA Score"] = 2
        elif roa > 0:
            score["ROA Score"] = 1
        else:
            score["ROA Score"] = 0

    # Operating Margin
    if op_margin is not None:
        if op_margin > 0.3:
            score["Operating Margin Score"] = 5
        elif op_margin > 0.2:
            score["Operating Margin Score"] = 4
        elif op_margin > 0.1:
            score["Operating Margin Score"] = 3
        elif op_margin > 0.05:
            score["Operating Margin Score"] = 2
        elif op_margin > 0:
            score["Operating Margin Score"] = 1
        else:
            score["Operating Margin Score"] = 0

    # Gross Margin
    if gross_margin is not None:
        if gross_margin > 0.6:
            score["Gross Margin Score"] = 5
        elif gross_margin > 0.4:
            score["Gross Margin Score"] = 4
        elif gross_margin > 0.3:
            score["Gross Margin Score"] = 3
        elif gross_margin > 0.2:
            score["Gross Margin Score"] = 2
        elif gross_margin > 0:
            score["Gross Margin Score"] = 1
        else:
            score["Gross Margin Score"] = 0

    # Debt-to-Equity (lower is better)
    if debt is not None:
        if debt < 30:
            score["Debt to Equity Score"] = 5
        elif debt < 60:
            score["Debt to Equity Score"] = 4
        elif debt < 100:
            score["Debt to Equity Score"] = 3
        elif debt < 200:
            score["Debt to Equity Score"] = 2
        elif debt < 300:
            score["Debt to Equity Score"] = 1
        else:
            score["Debt to Equity Score"] = 0

    # Interest Coverage Ratio
    if interest_coverage is not None:
        if interest_coverage > 20:
            score["Interest Coverage Score"] = 5
        elif interest_coverage > 10:
            score["Interest Coverage Score"] = 4
        elif interest_coverage > 5:
            score["Interest Coverage Score"] = 3
        elif interest_coverage > 2:
            score["Interest Coverage Score"] = 2
        elif interest_coverage > 0:
            score["Interest Coverage Score"] = 1
        else:
            score["Interest Coverage Score"] = 0

    score["Total"] = sum(score.values())
    return score


