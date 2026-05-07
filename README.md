# 📈 Stock Market Data Analyzer

> **⚠️ DISCLAIMER:** This project is for **educational purposes only**. It does **NOT** constitute financial advice. Past performance does not guarantee future results. Always consult a qualified financial advisor before making any investment decisions.

---

## 📌 Project Overview

**Stock Market Data Analyzer** is a complete Python-based data analysis project that:

- Fetches historical stock price data from **Yahoo Finance** (via `yfinance`)
- Cleans and validates OHLCV (Open, High, Low, Close, Volume) data
- Computes technical indicators: **SMA, EMA, Bollinger Bands, RSI, MACD, Returns, Volatility**
- Calculates risk metrics: **Sharpe Ratio, Max Drawdown, VaR**
- Generates **25 professional charts** (8 per ticker + 1 comparison)
- Produces a complete **text report + CSV summary**
- Includes a full **interactive Streamlit dashboard** with 7 tabs

---

## 🎯 Problem Statement

Most beginner investors and analysts:
- ❌ Cannot afford Bloomberg or Reuters terminals
- ❌ Manually track stocks in spreadsheets — slow and error-prone
- ❌ Have no way to quantify risk of their holdings
- ❌ Cannot visualise trends, moving averages, or historical drawdowns

This project solves all of this using **100% free, open-source Python tools**.

---

## 🏭 Industry Relevance

| Role | How This Project Helps |
|------|------------------------|
| Python Developer | Modular code, CLI, file I/O, data pipelines |
| Data Analyst | Pandas, NumPy, time-series EDA, descriptive stats |
| Financial Analyst | Price trends, moving averages, risk/return metrics |
| Business Analyst | Comparison reports, CSV summaries, chart interpretation |
| FinTech Role | End-to-end automation pipeline with clean outputs |

**Companies using similar Python pipelines:** Zerodha Kite, Groww Research, Smallcase, HDFC Securities, Upstox — all use Python + Pandas for market data analysis internally.

---

## ✨ Features

| Feature | Details |
|---------|---------|
| **Data Ingestion** | Yahoo Finance via `yfinance` + local CSV fallback |
| **Data Cleaning** | Duplicate removal, NaN handling, type fixing |
| **EDA** | Descriptive stats, year-wise summary, best/worst days |
| **Moving Averages** | SMA-20, SMA-50, SMA-200, EMA-20 |
| **Signals** | Golden Cross ▲, Death Cross ▼, BUY/SELL signal |
| **Returns** | Daily return, log return, cumulative return |
| **Risk Analysis** | Sharpe ratio, max drawdown, VaR 95%, annual volatility |
| **Technical Indicators** | RSI (14), MACD (12-26-9), Bollinger Bands |
| **Charts** | 8 charts per ticker + 1 multi-ticker comparison (25 total) |
| **Report** | Full text report + CSV summary saved to `reports/` |
| **Dashboard** | Interactive Streamlit app with 7 analysis tabs |

---

## 🛠 Tech Stack

```
Python 3.11
├── pandas        → Data manipulation and time-series operations
├── numpy         → Numerical calculations (returns, volatility)
├── yfinance      → Yahoo Finance data fetching (free API)
├── matplotlib    → All chart plotting
├── seaborn       → Monthly heatmap styling
├── streamlit     → Interactive web dashboard
├── plotly        → Interactive Plotly charts in dashboard
└── datetime      → Date range handling
```

No paid APIs. No external databases. No backend servers required.

---

## 🏗 Architecture & Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│               STOCK MARKET DATA ANALYZER PIPELINE               │
└─────────────────────────────────────────────────────────────────┘

INPUT
┌────────────────────────────────────────────────────────────────┐
│  Ticker Symbol (AAPL, MSFT, GOOGL)  │  Date Range (2018-2024) │
└──────────────────────────┬─────────────────────────────────────┘
                           │
                           ▼
STEP 1 — DATA COLLECTION
┌────────────────────────────────────────────────────────────────┐
│  yfinance.download()  →  OHLCV DataFrame  →  data/TICKER_raw.csv│
└──────────────────────────┬─────────────────────────────────────┘
                           ▼
STEP 2 — DATA CLEANING
┌────────────────────────────────────────────────────────────────┐
│  Remove duplicates → Fill NaN → Fix types → data/TICKER_clean.csv│
└──────────────────────────┬─────────────────────────────────────┘
                           ▼
STEP 3 — EXPLORATORY DATA ANALYSIS
┌────────────────────────────────────────────────────────────────┐
│  Descriptive stats │ Year-wise summary │ Best/worst days        │
│  → outputs/eda_summary.csv                                      │
└──────────────────────────┬─────────────────────────────────────┘
                           ▼
STEP 4 — MOVING AVERAGES & RETURNS
┌────────────────────────────────────────────────────────────────┐
│  SMA-20/50/200 │ EMA-20 │ Daily Return │ Cumulative Return      │
│  Golden Cross ▲ │ Death Cross ▼  →  data/TICKER_indicators.csv │
└──────────────────────────┬─────────────────────────────────────┘
                           ▼
STEP 5 — RISK & VOLATILITY ANALYSIS
┌────────────────────────────────────────────────────────────────┐
│  Sharpe Ratio │ Annual Volatility │ Max Drawdown │ VaR 95%      │
│  → outputs/risk_summary.csv                                     │
└──────────────────────────┬─────────────────────────────────────┘
                           ▼
STEP 6 — VISUALIZATION (25 CHARTS)
┌────────────────────────────────────────────────────────────────┐
│  Chart 1: Price + Volume                                        │
│  Chart 2: Price + SMA-20/50/200 + Golden/Death Cross            │
│  Chart 3: Bollinger Bands                                       │
│  Chart 4: Daily Returns (bar + distribution histogram)          │
│  Chart 5: Cumulative Return                                     │
│  Chart 6: Rolling 20-day Volatility                             │
│  Chart 7: Drawdown Chart                                        │
│  Chart 8: Monthly Returns Heatmap                               │
│  Chart 9: Multi-Ticker Comparison   →  outputs/*.png            │
└──────────────────────────┬─────────────────────────────────────┘
                           ▼
STEP 7 — REPORT GENERATION
┌────────────────────────────────────────────────────────────────┐
│  reports/stock_analysis_report.txt                              │
│  reports/risk_return_summary.csv                                │
└────────────────────────────────────────────────────────────────┘
                           ▼
STREAMLIT DASHBOARD (dashboard.py)
┌────────────────────────────────────────────────────────────────┐
│  Tab 1: Price & Moving Averages (Candlestick + BB + Volume)     │
│  Tab 2: Returns & Risk (Cumulative, Distribution, Drawdown)     │
│  Tab 3: Indicators (RSI, MACD, BB Width)                        │
│  Tab 4: Monthly Heatmap (Year × Month grid)                     │
│  Tab 5: Multi-Ticker Comparison                                 │
│  Tab 6: Raw Data Table + CSV Download                           │
│  Tab 7: Automated Insights + Downloadable Report                │
└────────────────────────────────────────────────────────────────┘
```

---

## 📁 Folder Structure

```
Stock-Market-Data-Analyzer/
│
├── data/                          ← CSV files (raw + cleaned + indicators)
│   ├── AAPL_raw.csv
│   ├── AAPL_clean.csv
│   ├── AAPL_indicators.csv
│   ├── MSFT_*.csv
│   └── GOOGL_*.csv
│
├── src/                           ← Python source modules (one per step)
│   ├── step1_data_collection.py   ← Yahoo Finance fetch + CSV fallback
│   ├── step2_data_cleaning.py     ← Clean, validate, normalise
│   ├── step3_eda.py               ← Exploratory Data Analysis
│   ├── step4_moving_averages.py   ← SMA/EMA/Returns/Signals
│   ├── step5_risk_analysis.py     ← Sharpe/MaxDD/VaR/Volatility
│   ├── step6_visualization.py     ← 8 charts per ticker (25 total)
│   └── step7_report.py            ← Text + CSV report generator
│
├── outputs/                       ← 25 PNG charts saved here
│   ├── AAPL_01_price_volume.png
│   ├── AAPL_02_moving_averages.png
│   ├── AAPL_03_bollinger_bands.png
│   ├── AAPL_04_daily_returns.png
│   ├── AAPL_05_cumulative_return.png
│   ├── AAPL_06_rolling_volatility.png
│   ├── AAPL_07_drawdown.png
│   ├── AAPL_08_monthly_heatmap.png
│   ├── MSFT_*.png  (8 charts)
│   ├── GOOGL_*.png (8 charts)
│   ├── comparison_cumulative_return.png
│   ├── eda_summary.csv
│   └── risk_summary.csv
│
├── reports/                       ← Final analysis reports
│   ├── stock_analysis_report.txt
│   └── risk_return_summary.csv
│
├── images/                        ← Screenshots for this README
├── notebooks/                     ← Jupyter notebooks (optional EDA)
├── docs/                          ← Additional documentation
│
├── main.py                        ← 🚀 Run this to execute full pipeline
├── dashboard.py                   ← 🖥 Run this for Streamlit dashboard
├── requirements.txt               ← All Python dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Installation Guide

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Stock-Market-Data-Analyzer.git
cd Stock-Market-Data-Analyzer
```

### Step 2 — Create virtual environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

### 🔥 Option A — Run full pipeline (recommended)

```bash
python main.py
```

**Terminal Output:**
```
╔══════════════════════════════════════════════════════════╗
║         📈  STOCK MARKET DATA ANALYZER  📈              ║
╚══════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ▶  STEP 1/7 — STOCK DATA COLLECTION (Yahoo Finance)
[INFO] Fetching AAPL from Yahoo Finance (2018-01-01 → 2024-12-31) ...
[OK]   AAPL — 1762 rows fetched.
[SAVED] data/AAPL_raw.csv
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ▶  STEP 6/7 — VISUALIZATION (8 CHARTS PER TICKER)
  [SAVED] outputs/AAPL_01_price_volume.png
  [SAVED] outputs/AAPL_02_moving_averages.png
  ... (25 charts total)

╔══════════════════════════════════════════════════════════╗
║                ✅  PIPELINE COMPLETE                     ║
║  📁 data/    → 9 CSV files                               ║
║  📊 outputs/ → 25 PNG charts                             ║
║  📄 reports/ → .txt Report + .csv Summary                ║
╚══════════════════════════════════════════════════════════╝
```

### 🖥 Option B — Launch Streamlit Dashboard

```bash
streamlit run dashboard.py
```

Opens at: **http://localhost:8501**

Dashboard features 7 interactive tabs:
- 📊 Price & Moving Averages (Candlestick + Bollinger Bands)
- 📉 Returns & Risk (Cumulative return, VaR, Drawdown)
- 🔬 Technical Indicators (RSI, MACD, BB Width)
- 🗓 Monthly Heatmap
- ⚖️ Multi-ticker Comparison
- 📋 Raw Data + CSV Download
- 💡 Automated Insights + Report

### Option C — Analyse custom tickers

```bash
python main.py --tickers TSLA NVDA RELIANCE.NS
```

### Option D — Run steps individually

```bash
python src/step1_data_collection.py   # Fetch data
python src/step2_data_cleaning.py     # Clean data
python src/step3_eda.py               # EDA statistics
python src/step4_moving_averages.py   # Compute indicators
python src/step5_risk_analysis.py     # Risk metrics
python src/step6_visualization.py     # Generate all charts
python src/step7_report.py            # Generate report
```

### Option E — No internet? Use sample data

```bash
python generate_sample_data.py   # generates realistic OHLCV CSV files
python main.py                   # then run normally
```

---

## 📊 Sample Output

### Terminal (Step 5 Risk Analysis)
```
  ── Return ──────────────────────────────────────────────
  Total Return          :    322.27%
  Annualised Return     :     21.99%
  Avg Daily Return      :    0.0897%
  Positive Days         :       974 (53.3%)
  Best Single Day       :    5.8888%
  Worst Single Day      :   -8.1455%

  ── Risk ────────────────────────────────────────────────
  Daily Volatility      :    1.4697%
  Annual Volatility     :     23.33%
  Sharpe Ratio          :    0.9691
  Maximum Drawdown      :    -55.32%
  VaR (95%, 1-day)      :   -2.2113%
```

### Generated Charts (outputs/)

| File | What it shows |
|------|--------------|
| `AAPL_01_price_volume.png` | Closing price with volume bars |
| `AAPL_02_moving_averages.png` | SMA-20/50/200 + Golden/Death crosses |
| `AAPL_03_bollinger_bands.png` | Bollinger bands (20-day, 2σ) |
| `AAPL_04_daily_returns.png` | Daily return bars + distribution |
| `AAPL_05_cumulative_return.png` | Compounded return since 2018 |
| `AAPL_06_rolling_volatility.png` | 20-day rolling annualised volatility |
| `AAPL_07_drawdown.png` | Equity curve + drawdown chart |
| `AAPL_08_monthly_heatmap.png` | Year × Month return heatmap |
| `comparison_cumulative_return.png` | AAPL vs MSFT vs GOOGL |

---

## 📸 Screenshots

> Add screenshots to `images/` after running the project:

| Screenshot | What to capture |
|-----------|----------------|
| `images/01_folder_structure.png` | Project folder in VS Code/Explorer |
| `images/02_terminal_step1.png` | Step 1 data fetch output |
| `images/03_terminal_step5.png` | Risk analysis terminal output |
| `images/04_AAPL_price_chart.png` | AAPL_02_moving_averages.png |
| `images/05_bollinger.png` | AAPL_03_bollinger_bands.png |
| `images/06_returns_dist.png` | AAPL_04_daily_returns.png |
| `images/07_heatmap.png` | AAPL_08_monthly_heatmap.png |
| `images/08_comparison.png` | comparison_cumulative_return.png |
| `images/09_dashboard.png` | Streamlit dashboard screenshot |
| `images/10_report_output.png` | reports/stock_analysis_report.txt |
| `images/11_github_repo.png` | Your GitHub repo page |

---

## 🎓 Learning Outcomes

After completing this project you will know:

**Python Skills**
- Structuring a multi-module Python project
- Argparse CLI with flags and arguments
- Reading/writing CSV files with Pandas
- Working with datetime index in time-series
- Building interactive web apps with Streamlit

**Data Analysis**
- OHLCV data structure and meaning of each column
- How to calculate percentage returns correctly
- What moving averages show and how to interpret crossovers
- How rolling windows work (`df.rolling(20).mean()`)

**Financial Concepts**
- What is a Sharpe ratio and why it matters
- How to compute and interpret maximum drawdown
- What Bollinger Bands indicate about price volatility
- What Value at Risk (VaR) means in practice
- Golden Cross vs Death Cross signals
- RSI and MACD momentum indicators

**Visualisation**
- Multi-panel `GridSpec` Matplotlib figures
- Seaborn heatmaps for monthly data
- Dark-themed professional Plotly charts
- Interactive Streamlit dashboards
- Saving charts as PNG for GitHub

---

## 🗓 GitHub Proof-of-Work Plan (6 Days)

| Day | Task | What to Commit |
|-----|------|---------------|
| **Day 1** | Project setup + folder structure | `feat: initialise project structure and requirements` |
| **Day 2** | Step 1 + Step 2 | `feat: add data collection and cleaning modules` |
| **Day 3** | Step 3 + Step 4 | `feat: add EDA and moving average computation` |
| **Day 4** | Step 5 | `feat: add risk and volatility analysis` |
| **Day 5** | Step 6 | `feat: generate 25 visualisation charts` |
| **Day 6** | Step 7 + dashboard + README + outputs | `docs: final report, dashboard, README, charts, screenshots` |

### GitHub Repository Settings

**Repo name:** `Stock-Market-Data-Analyzer`
**Description:** `Python project that analyzes stock market data using pandas, numpy, matplotlib, plotly and yfinance. Includes Streamlit dashboard with 7 analysis tabs. Computes moving averages, RSI, MACD, returns, risk metrics and generates charts. Educational purposes only.`

**Topics to add:**
```
python  stock-market  data-analysis  pandas  numpy  matplotlib
yfinance  financial-analysis  data-visualization  student-project
moving-averages  risk-analysis  time-series  eda  seaborn
streamlit  plotly  dashboard  rsi  macd
```

---

## ⚠️ Disclaimer

> This project is built for **EDUCATIONAL PURPOSES ONLY** as part of a Python course.
> It does **NOT** provide investment, financial, or trading advice.
> The author(s) are **NOT** SEBI-registered advisors.
> Do **NOT** use this project to make real investment decisions.
> Always consult a qualified financial advisor.

---

*Made with ❤️ | Star ⭐ this repo if it helped you!*