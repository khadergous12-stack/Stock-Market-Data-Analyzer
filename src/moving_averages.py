"""
=============================================================
 STOCK MARKET DATA ANALYZER
 Step 4 — Moving Averages & Returns Calculation
 Input : data/{TICKER}_clean.csv
 Output: data/{TICKER}_indicators.csv
=============================================================
 DISCLAIMER: Educational purposes only. Not financial advice.
=============================================================
"""

import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
TICKERS  = ["AAPL", "MSFT", "GOOGL"]


def compute_moving_averages_and_returns(df: pd.DataFrame, ticker: str) -> pd.DataFrame:
    """
    Add the following columns to the DataFrame:

    Moving Averages:
        SMA_20   — 20-day Simple Moving Average
        SMA_50   — 50-day Simple Moving Average
        SMA_200  — 200-day Simple Moving Average
        EMA_20   — 20-day Exponential Moving Average

    Returns:
        Daily_Return      — % change in Close price
        Log_Return        — natural log of daily ratio
        Cumulative_Return — running compounded return from Day 1

    Volatility:
        Rolling_Vol_20    — 20-day rolling std of daily return (annualised)

    Signals:
        Signal            — BUY (SMA20 > SMA50), SELL otherwise
        Golden_Cross      — 1 where SMA20 just crossed above SMA50
        Death_Cross       — 1 where SMA20 just crossed below SMA50
    """
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    close      = df["Close"].astype(float)

    # ── Moving Averages ───────────────────────────────────────────────────────
    df["SMA_20"]  = close.rolling(window=20).mean().round(4)
    df["SMA_50"]  = close.rolling(window=50).mean().round(4)
    df["SMA_200"] = close.rolling(window=200).mean().round(4)
    df["EMA_20"]  = close.ewm(span=20, adjust=False).mean().round(4)

    # ── Returns ───────────────────────────────────────────────────────────────
    df["Daily_Return"]      = close.pct_change().round(6)
    df["Log_Return"]        = np.log(close / close.shift(1)).round(6)
    df["Cumulative_Return"] = ((1 + df["Daily_Return"]).cumprod() - 1).round(6)

    # ── Rolling Volatility (annualised) ───────────────────────────────────────
    df["Rolling_Vol_20"] = (df["Daily_Return"].rolling(20).std() * np.sqrt(252)).round(6)

    # ── Trend Signals ─────────────────────────────────────────────────────────
    df["Signal"]       = np.where(df["SMA_20"] > df["SMA_50"], "BUY", "SELL")
    prev_above         = (df["SMA_20"].shift(1) > df["SMA_50"].shift(1))
    curr_above         = (df["SMA_20"] > df["SMA_50"])
    df["Golden_Cross"] = ((~prev_above) & curr_above).astype(int)
    df["Death_Cross"]  = ((prev_above) & (~curr_above)).astype(int)

    # ── Summary Print ─────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  Indicators Computed — {ticker}")
    print(f"{'='*60}")
    print(f"  Latest SMA_20   : ${df['SMA_20'].dropna().iloc[-1]:.2f}")
    print(f"  Latest SMA_50   : ${df['SMA_50'].dropna().iloc[-1]:.2f}")
    print(f"  Latest SMA_200  : ${df['SMA_200'].dropna().iloc[-1]:.2f}")
    print(f"  Latest EMA_20   : ${df['EMA_20'].dropna().iloc[-1]:.2f}")
    print(f"  Current Signal  : {df['Signal'].iloc[-1]}")
    print(f"  Golden Crosses  : {df['Golden_Cross'].sum()}")
    print(f"  Death Crosses   : {df['Death_Cross'].sum()}")
    total = ((1 + df["Daily_Return"]).cumprod().iloc[-1] - 1) * 100
    print(f"  Total Return    : {total:.2f}%  (since {df['Date'].iloc[0].date()})")

    print(f"\n  Sample (last 5 rows with indicators):")
    cols = ["Date","Close","SMA_20","SMA_50","Daily_Return","Cumulative_Return","Signal"]
    print(df[cols].dropna().tail(5).to_string(index=False))

    return df


def compute_all():
    """Compute indicators for all tickers and save."""
    print("\n" + "="*60)
    print("  STEP 4 — MOVING AVERAGES & RETURNS")
    print("="*60)

    all_dfs = {}
    for ticker in TICKERS:
        path = os.path.join(DATA_DIR, f"{ticker}_clean.csv")
        if not os.path.exists(path):
            print(f"[SKIP] {path} not found.")
            continue
        df  = pd.read_csv(path)
        out = compute_moving_averages_and_returns(df, ticker)
        save_path = os.path.join(DATA_DIR, f"{ticker}_indicators.csv")
        out.to_csv(save_path, index=False)
        print(f"\n[SAVED] {save_path}")
        all_dfs[ticker] = out

    print("\n[DONE] Step 4 complete.")
    return all_dfs


if __name__ == "__main__":
    compute_all()
