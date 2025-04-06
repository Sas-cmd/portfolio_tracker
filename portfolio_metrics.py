import pandas as pd
import yfinance as yf
from typing import List, Dict, Any

def fetch_latest_prices(tickers: List[str]) -> Dict[str, float]:
    """Fetch the latest closing price for each ticker from Yahoo Finance."""
    prices = {}
    for ticker in tickers:
        try:
            tkr = yf.Ticker(ticker)
            hist = tkr.history(period="1d")
            if not hist.empty:
                prices[ticker] = hist["Close"].iloc[-1]
            else:
                # If no data is returned, store None or 0
                prices[ticker] = None
        except Exception:
            prices[ticker] = None
    return prices

def calculate_performance(transactions: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create a performance DataFrame with columns for P/L, etc."""
    if not transactions:
        return pd.DataFrame()

    # Convert list of dict to DataFrame
    df = pd.DataFrame(transactions)
    
    # Fetch current prices
    tickers = df["Ticker"].unique().tolist()
    latest_prices = fetch_latest_prices(tickers)

    performance_data = []
    for _, row in df.iterrows():
        ticker = row["Ticker"]
        shares = float(row["Shares"])
        invested = shares * float(row["Price Paid"])
        current_price = latest_prices.get(ticker, row["Price Paid"]) or row["Price Paid"]
        current_value = shares * current_price
        profit_loss = current_value - invested
        pl_percent = (profit_loss / invested) * 100 if invested > 0 else 0

        performance_data.append({
            "Stock": row["Stock"],
            "Ticker": ticker,
            "Shares": shares,
            "Avg Cost": row["Price Paid"],
            "Live Price": round(current_price, 2),
            "Invested ($)": round(invested, 2),
            "Current Value ($)": round(current_value, 2),
            "P/L ($)": round(profit_loss, 2),
            "P/L (%)": round(pl_percent, 2)
        })
    perf_df = pd.DataFrame(performance_data)
    return perf_df
