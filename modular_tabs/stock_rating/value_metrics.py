import streamlit as st
import yfinance as yf
import pandas as pd
from modular_tabs.stock_rating.data_fetcher import fetch_all_data, fetch_from_fmp
from .quality_metrics import fetch_quality_metrics
from modular_tabs.stock_rating.score_utils import score_to_badge

def fetch_value_metrics(ticker):
    try:
        data = fetch_all_data(ticker)
        info = data.get("info", {})
        cashflow = data.get("cashflow", None)

        pe_ratio = info.get("trailingPE")
        pb_ratio = info.get("priceToBook")
        eps_growth = info.get("earningsGrowth")
        market_cap = info.get("marketCap")
        ev = info.get("enterpriseValue")
        ebitda = info.get("ebitda")

        peg_ratio = (pe_ratio / eps_growth) if pe_ratio and eps_growth else None
        pb_ratio = info.get("priceToBook")

        fcf = None
        price_to_fcf = None

        try:
            if isinstance(cashflow, pd.DataFrame):
                if "Operating Cash Flow" in cashflow.index and "Capital Expenditure" in cashflow.index:
                    op_cf_series = cashflow.loc["Operating Cash Flow"].dropna()
                    capex_series = cashflow.loc["Capital Expenditure"].dropna()

                    if not op_cf_series.empty and not capex_series.empty:
                        op_cash_flow = op_cf_series.iloc[0]
                        capex = capex_series.iloc[0]

                        if isinstance(op_cash_flow, (int, float)) and isinstance(capex, (int, float)):
                            fcf = op_cash_flow + capex
                        else:
                            print("❌ Operating CF or CapEx is not a number")
                    else:
                        print("⚠️ Cashflow rows present but empty")
                else:
                    print("❌ Required cashflow rows not found.")
            else:
                print("⚠️ Cashflow is not a DataFrame — likely from fallback API")

            if market_cap and fcf and isinstance(fcf, (int, float)) and fcf != 0:
                price_to_fcf = market_cap / fcf
            else:
                print("⚠️ FCF or Market Cap invalid for Price/FCF calc")

        except Exception as e:
            print("Could not compute FCF:", e)

        ev_to_ebitda = (ev / ebitda) if ev and ebitda and ebitda != 0 else None
        earnings_yield = (1 / pe_ratio) if pe_ratio and pe_ratio != 0 else None

        return {
            "P/E Ratio": pe_ratio,
            "P/B Ratio": pb_ratio,
            "PEG Ratio": peg_ratio,
            "Price to FCF": price_to_fcf,
            "EV/EBITDA": ev_to_ebitda,
            "Earnings Yield": earnings_yield
        }

    except Exception as e:
        print(f"Error fetching value metrics: {e}")
        return {}
    

def score_value(pe, pb, peg, fcf_ratio, ev_ebitda, earnings_yield):
    score = {}

    def badge(val): return score_to_badge(val)

    # P/E Ratio
    if pe is not None:
        if pe < 15:
            score["P/E Ratio Score"] = 5
        elif pe < 25:
            score["P/E Ratio Score"] = 4
        elif pe < 35:
            score["P/E Ratio Score"] = 3
        elif pe < 50:
            score["P/E Ratio Score"] = 2
        elif pe < 75:
            score["P/E Ratio Score"] = 1
        else:
            score["P/E Ratio Score"] = 0

    # P/B Ratio
    if pb is not None:
        if pb < 1:
            score["P/B Ratio Score"] = 5
        elif pb < 2:
            score["P/B Ratio Score"] = 4
        elif pb < 3:
            score["P/B Ratio Score"] = 3
        elif pb < 5:
            score["P/B Ratio Score"] = 2
        elif pb < 7:
            score["P/B Ratio Score"] = 1
        else:
            score["P/B Ratio Score"] = 0

    # PEG Ratio
    if peg is not None:
        if peg < 1:
            score["PEG Ratio Score"] = 5
        elif peg < 1.5:
            score["PEG Ratio Score"] = 4
        elif peg < 2:
            score["PEG Ratio Score"] = 3
        elif peg < 2.5:
            score["PEG Ratio Score"] = 2
        elif peg < 3:
            score["PEG Ratio Score"] = 1
        else:
            score["PEG Ratio Score"] = 0

    # Price to FCF
    if fcf_ratio is not None:
        if fcf_ratio < 10:
            score["Price to FCF Score"] = 5
        elif fcf_ratio < 15:
            score["Price to FCF Score"] = 4
        elif fcf_ratio < 20:
            score["Price to FCF Score"] = 3
        elif fcf_ratio < 30:
            score["Price to FCF Score"] = 2
        elif fcf_ratio < 40:
            score["Price to FCF Score"] = 1
        else:
            score["Price to FCF Score"] = 0

    # EV/EBITDA
    if ev_ebitda is not None:
        if ev_ebitda < 8:
            score["EV/EBITDA Score"] = 5
        elif ev_ebitda < 10:
            score["EV/EBITDA Score"] = 4
        elif ev_ebitda < 15:
            score["EV/EBITDA Score"] = 3
        elif ev_ebitda < 20:
            score["EV/EBITDA Score"] = 2
        elif ev_ebitda < 30:
            score["EV/EBITDA Score"] = 1
        else:
            score["EV/EBITDA Score"] = 0

    # Earnings Yield
    if earnings_yield is not None:
        if earnings_yield > 0.08:
            score["Earnings Yield Score"] = 5
        elif earnings_yield > 0.06:
            score["Earnings Yield Score"] = 4
        elif earnings_yield > 0.04:
            score["Earnings Yield Score"] = 3
        elif earnings_yield > 0.02:
            score["Earnings Yield Score"] = 2
        elif earnings_yield > 0:
            score["Earnings Yield Score"] = 1
        else:
            score["Earnings Yield Score"] = 0

    score["Total"] = sum(score.values())
    return score


def score_quality(roe, roa, op_margin, gross_margin, debt, interest_coverage):
    score = {}

    # ROE
    if roe is not None:
        if roe > 0.2:
            score["ROE Score"] = 5
        elif roe > 0.1:
            score["ROE Score"] = 3
        elif roe > 0.05:
            score["ROE Score"] = 1
        else:
            score["ROE Score"] = 0

    # ROA
    if roa is not None:
        if roa > 0.1:
            score["ROA Score"] = 5
        elif roa > 0.05:
            score["ROA Score"] = 3
        elif roa > 0.02:
            score["ROA Score"] = 1
        else:
            score["ROA Score"] = 0

    # Operating Margin
    if op_margin is not None:
        if op_margin > 0.2:
            score["Operating Margin Score"] = 5
        elif op_margin > 0.1:
            score["Operating Margin Score"] = 3
        elif op_margin > 0.05:
            score["Operating Margin Score"] = 1
        else:
            score["Operating Margin Score"] = 0

    # Gross Margin
    if gross_margin is not None:
        if gross_margin > 0.5:
            score["Gross Margin Score"] = 5
        elif gross_margin > 0.3:
            score["Gross Margin Score"] = 3
        elif gross_margin > 0.1:
            score["Gross Margin Score"] = 1
        else:
            score["Gross Margin Score"] = 0

    # Debt-to-Equity
    if debt is not None:
        if debt < 50:
            score["Debt to Equity Score"] = 5
        elif debt < 100:
            score["Debt to Equity Score"] = 3
        elif debt < 200:
            score["Debt to Equity Score"] = 1
        else:
            score["Debt to Equity Score"] = 0

    # Interest Coverage
    if interest_coverage is not None:
        if interest_coverage > 10:
            score["Interest Coverage Score"] = 5
        elif interest_coverage > 5:
            score["Interest Coverage Score"] = 3
        elif interest_coverage > 2:
            score["Interest Coverage Score"] = 1
        else:
            score["Interest Coverage Score"] = 0

    # Total
    score["Total"] = sum(score.values())
    return score

def overall_rating(value_score, quality_score):
    # Compute final rating based on combined score
    total = value_score + quality_score

    if total >= 45:
        return "Very Strong Buy", total

    elif total >= 35:
        return "Strong Buy", total
    
    elif total >= 25:
        return "Buy", total
    
    elif total >= 15:
        return "Hold", total
    
    else:
        return "Sell", total

def rate_stock(ticker):
    value_metrics = fetch_value_metrics(ticker)
    quality_metrics = fetch_quality_metrics(ticker)

    value_score = score_value(
        value_metrics.get("P/E Ratio"),
        value_metrics.get("P/B Ratio"),
        value_metrics.get("PEG Ratio"),
        value_metrics.get("Price to FCF"),
        value_metrics.get("EV/EBITDA"),
        value_metrics.get("Earnings Yield")
    )

    quality_score = score_quality(
        quality_metrics.get("ROE"),
        quality_metrics.get("ROA"),
        quality_metrics.get("Operating Margin"),
        quality_metrics.get("Gross Margin"),
        quality_metrics.get("Debt to Equity"),
        quality_metrics.get("Interest Coverage Ratio")
    )
    
    value_total = value_score.get("Total", 0)
    quality_total = quality_score.get("Total", 0)
    rating, total_score = overall_rating(value_total, quality_total)

    all_metrics = {
        **value_metrics,
        **quality_metrics,
        **value_score,
        **quality_score,
    }

    return rating, {
        "Value Score": value_total,
        "Quality Score": quality_total,
        "Total Score": total_score,
        "Fundamentals": all_metrics,
    }