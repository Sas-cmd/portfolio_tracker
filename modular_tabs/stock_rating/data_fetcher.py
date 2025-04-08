import yfinance as yf
import requests

MARKETSTACK_API_KEY = "2a477a2008418393665fc7a9eaf64815"
FMP_API_KEY = "o6MvC597oltamnoeWG9AUk4k2bQvbxSX"

def fetch_all_data(ticker: str) -> dict:
    try:
        data = fetch_from_yfinance(ticker)
        if data and data.get("valid", False):
            data["source"] = "yfinance"
            return data
        else:
            raise ValueError("Data missing or invalid from yfinance")
    except Exception as e:
        print(f"⚠️ yfinance failed: {e}")
        try:
            return fetch_from_marketstack(ticker)
        except Exception as e:
            print(f"⚠️ marketstack failed: {e}")
            return fetch_from_fmp(ticker)

def fetch_from_yfinance(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        cashflow = stock.cashflow
        financials = stock.financials
        balance = stock.balance_sheet
        income = stock.income_stmt 

        return {
            "info": info,
            "cashflow": cashflow,
            "financials": financials,
            "balance_sheet": balance,
            "income_statement": income,
            "valid": isinstance(info, dict) and len(info) > 0
        }
    except Exception as e:
        print(f"❌ yfinance error: {e}")
        return {"valid": False}

def fetch_from_marketstack(ticker):
    try:
        url = f"http://api.marketstack.com/v1/eod?access_key={MARKETSTACK_API_KEY}&symbols={ticker}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return {
            "info": data.get("data", []),
            "cashflow": None,
            "valid": "data" in data and len(data["data"]) > 0
        }
    except Exception as e:
        print(f"❌ Marketstack error: {e}")
        return {"valid": False}

def fetch_from_fmp(ticker):
    try:
        profile_url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={FMP_API_KEY}"
        ratios_url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{ticker}?apikey={FMP_API_KEY}"

        profile = requests.get(profile_url).json()
        ratios = requests.get(ratios_url).json()

        return {
            "info": profile[0] if profile else {},
            "ratios": ratios[0] if ratios else {},
            "income_statement": {},   
            "balance_sheet": {},
            "cashflow": {},
            "source": "fmp",
            "valid": bool(profile)
        }
    except Exception as e:
        print(f"❌ FMP error: {e}")
        return {"valid": False}