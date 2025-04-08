# Portfolio Tracker

A powerful Streamlit tool for analyzing portfolio performance, monitoring markets, and making smarter investment decisions. Includes import/export functionality, risk and scenario simulation, contribution forecasting, a personalized watchlist, and smart alerts — all designed to future-proof your investment strategy.

---

## Features
- **Real-Time Portfolio Summary** – Track your investments with live market prices
- **Transaction Management** – Add, view, and delete purchases with an intuitive UI
- **Visual Insights** – Pie and bar charts to break down allocations and performance
- **Market Trends Viewer** – Historical charts with buy markers and timeframe filters
- **Import/Export** – Seamless CSV or JSON support for backing up or transferring data
- **Scenario Analysis** – Model downturns and recovery simulations for long-term planning
- **Contribution Planner** – Forecast future portfolio growth
- **Watchlist** – Keep tabs on future investment opportunities
- **Notifications (Planned)** – Custom alerts for price movements or contributions

---

## Tech Stack
- **Frontend/UI**: [Streamlit](https://streamlit.io/)
- **Data Handling**: `pandas`, `json`, `datetime`
- **Market Data**: [yFinance](https://pypi.org/project/yfinance/)
- **Visualization**: `matplotlib` (or `plotly`)

---

## Getting Started

```bash
# 1. Clone this repository
git clone https://github.com/your-username/portfolio_tracker.git
cd portfolio_tracker

# 2. Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py


