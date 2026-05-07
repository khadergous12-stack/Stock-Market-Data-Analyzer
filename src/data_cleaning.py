"""
=============================================================
 STOCK MARKET DATA ANALYZER
 Step 2 — Data Cleaning
 Input : data/{TICKER}_raw.csv
 Output: data/{TICKER}_clean.csv
=============================================================
 DISCLAIMER: Educational purposes only. Not financial advice.
=============================================================
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TICKERS  = ["AAPL", "MSFT", "GOOGL"]


def clean_stock_data(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Full data cleaning pipeline:
      1. Parse and sort dates
      2. Remove duplicate rows
      3. Handle missing values
      4. Remove zero-price rows (bad data)
      5. Fix data types
      6. Add derived helper columns
    Returns the cleaned DataFrame.
    """
    print(f"\n{'='*55}")
    print(f"  Cleaning {ticker}")
    print(f"{'='*55}")

    original_len = len(df)

    # ── 1. Parse dates ────────────────────────────────────────────────────────
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    # ── 2. Remove duplicate dates ─────────────────────────────────────────────
    dupes = df.duplicated(subset="Date").sum()
    df = df.drop_duplicates(subset="Date").reset_index(drop=True)
    print(f"  Duplicate rows removed  : {dupes}")

    # ── 3. Handle missing values ──────────────────────────────────────────────
    before_na = df.isnull().sum().sum()
    # Forward-fill then backward-fill (standard for OHLCV time series)
    df[["Open","High","Low","Close","Adj_Close"]] = (
        df[["Open","High","Low","Close","Adj_Close"]]
        .ffill().bfill()
    )
    df["Volume"] = df["Volume"].fillna(0).astype(int)
    after_na = df.isnull().sum().sum()
    print(f"  Missing values filled   : {before_na - after_na}")
    print(f"  Remaining NaN           : {after_na}")

    # ── 4. Remove bad rows (zero or negative prices) ──────────────────────────
    bad_rows = (df["Close"] <= 0).sum()
    df = df[df["Close"] > 0].reset_index(drop=True)
    print(f"  Bad price rows removed  : {bad_rows}")

    # ── 5. Ensure correct types ───────────────────────────────────────────────
    for col in ["Open", "High", "Low", "Close", "Adj_Close"]:
        df[col] = df[col].astype(float).round(4)
    df["Volume"] = df["Volume"].astype(int)

    # ── 6. Add helper columns ─────────────────────────────────────────────────
    df["Year"]  = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"]   = df["Date"].dt.day
    df["Weekday"] = df["Date"].dt.day_name()

    # Daily price range (High - Low)
    df["Daily_Range"] = (df["High"] - df["Low"]).round(4)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n  Rows: {original_len} → {len(df)}")
    print(f"  Period: {df['Date'].min().date()}  →  {df['Date'].max().date()}")
    print(f"\n  Clean Data Sample:")
    print(df[["Date","Open","High","Low","Close","Volume"]].head(3).to_string(index=False))
    print(f"  ...")
    print(df[["Date","Open","High","Low","Close","Volume"]].tail(3).to_string(index=False))

    return df


def clean_all():
    """Load raw CSVs, clean them, and save cleaned versions."""
    print("\n" + "="*55)
    print("  STEP 2 — DATA CLEANING")
    print("="*55)

    all_clean = {}
    for ticker in TICKERS:
        raw_path = os.path.join(DATA_DIR, f"{ticker}_raw.csv")
        if not os.path.exists(raw_path):
            print(f"[SKIP] {raw_path} not found. Run Step 1 first.")
            continue

        df_raw   = pd.read_csv(raw_path)
        df_clean = clean_stock_data(df_raw, ticker)

        clean_path = os.path.join(DATA_DIR, f"{ticker}_clean.csv")
        df_clean.to_csv(clean_path, index=False)
        print(f"\n[SAVED] {clean_path}")
        all_clean[ticker] = df_clean

    print("\n[DONE] Step 2 complete. Cleaned data saved to data/ folder.")
    return all_clean


if __name__ == "__main__":
    clean_all()
