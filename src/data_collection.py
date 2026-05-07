"""
=============================================================
 STOCK MARKET DATA ANALYZER
 Step 1 — Data Collection
 Tool : yfinance (Yahoo Finance) + CSV fallback
 Output: data/AAPL_raw.csv, data/MSFT_raw.csv, data/GOOGL_raw.csv
=============================================================
 DISCLAIMER: Educational purposes only. Not financial advice.
=============================================================
"""

import os
import datetime as dt
import pandas as pd
import yfinance as yf

# ── Config ────────────────────────────────────────────────────────────────────
TICKERS    = ["AAPL", "MSFT", "GOOGL"]
START_DATE = "2018-01-01"
END_DATE   = "2024-12-31"
DATA_DIR   = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)


# ── Function: Fetch from Yahoo Finance ───────────────────────────────────────
def fetch_stock_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """
    Fetch daily OHLCV data from Yahoo Finance.
    Returns a clean DataFrame with columns:
        Date, Open, High, Low, Close, Adj Close, Volume
    """
    print(f"\n[INFO] Fetching {ticker} from Yahoo Finance ({start} → {end}) ...")
    df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)

    if df.empty:
        raise ValueError(f"No data returned for {ticker}. Check the ticker symbol.")

    # Flatten multi-level columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df = df.rename(columns={"Adj Close": "Adj_Close"})
    df = df[["Date", "Open", "High", "Low", "Close", "Adj_Close", "Volume"]]
    df = df.sort_values("Date").reset_index(drop=True)

    print(f"[OK]   {ticker} — {len(df)} rows fetched.")
    return df


# ── Function: Load from local CSV (Fallback) ─────────────────────────────────
def load_csv_fallback(filepath: str) -> pd.DataFrame:
    """
    Load OHLCV data from a local CSV file when internet is unavailable.
    Expected columns: Date, Open, High, Low, Close, Volume
    (Adj Close is optional)
    """
    df = pd.read_csv(filepath, parse_dates=["Date"])
    df.columns = [c.strip() for c in df.columns]
    if "Adj Close" in df.columns:
        df = df.rename(columns={"Adj Close": "Adj_Close"})
    elif "Adj_Close" not in df.columns:
        df["Adj_Close"] = df["Close"]
    df = df.sort_values("Date").reset_index(drop=True)
    print(f"[OK]   Loaded {len(df)} rows from CSV → {filepath}")
    return df


# ── Function: Preview dataset ────────────────────────────────────────────────
def preview_data(df: pd.DataFrame, ticker: str):
    """Print a quick summary of the fetched dataset."""
    print(f"\n{'='*55}")
    print(f"  {ticker} — Dataset Preview")
    print(f"{'='*55}")
    print(f"  Shape      : {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"  Date Range : {df['Date'].min()}  →  {df['Date'].max()}")
    print(f"  Columns    : {list(df.columns)}")
    print(f"\n  First 5 rows:")
    print(df.head().to_string(index=False))
    print(f"\n  Last 5 rows:")
    print(df.tail().to_string(index=False))
    print(f"\n  Data Types:")
    print(df.dtypes.to_string())
    print(f"\n  Missing Values: {df.isnull().sum().sum()}")


# ── Main ──────────────────────────────────────────────────────────────────────
def collect_all():
    """Fetch and save data for all tickers."""
    print("\n" + "="*55)
    print("  STEP 1 — STOCK DATA COLLECTION")
    print("="*55)

    all_data = {}
    for ticker in TICKERS:
        try:
            df = fetch_stock_data(ticker, START_DATE, END_DATE)
            save_path = os.path.join(DATA_DIR, f"{ticker}_raw.csv")
            df.to_csv(save_path, index=False)
            print(f"[SAVED] {save_path}")
            preview_data(df, ticker)
            all_data[ticker] = df
        except Exception as e:
            print(f"[ERROR] Failed for {ticker}: {e}")

    print("\n[DONE] Step 1 complete. Raw data saved to data/ folder.")
    return all_data


if __name__ == "__main__":
    collect_all()
