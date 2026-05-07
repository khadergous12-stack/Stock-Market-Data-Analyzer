"""
=============================================================
 STOCK MARKET DATA ANALYZER
 Step 3 — Exploratory Data Analysis (EDA)
 Input : data/{TICKER}_clean.csv
 Output: Printed statistics + outputs/eda_summary.csv
=============================================================
 DISCLAIMER: Educational purposes only. Not financial advice.
=============================================================
"""

import os
import pandas as pd
import numpy as np

DATA_DIR    = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
TICKERS     = ["AAPL", "MSFT", "GOOGL"]
os.makedirs(OUTPUTS_DIR, exist_ok=True)


def eda_single(df: pd.DataFrame, ticker: str) -> dict:
    """
    Perform EDA on a single ticker DataFrame.
    Returns a summary dictionary.
    """
    df["Date"] = pd.to_datetime(df["Date"])
    close      = df["Close"]

    print(f"\n{'='*60}")
    print(f"  EDA — {ticker}")
    print(f"{'='*60}")

    # ── Descriptive Statistics ────────────────────────────────────────────────
    print("\n  Descriptive Statistics (Close Price):")
    stats = close.describe()
    for k, v in stats.items():
        print(f"    {k:<10} : {v:>10.4f}")

    # ── Price Extremes ────────────────────────────────────────────────────────
    idx_high = close.idxmax()
    idx_low  = close.idxmin()
    print(f"\n  All-Time High : ${close.max():.2f}  on {df.loc[idx_high,'Date'].date()}")
    print(f"  All-Time Low  : ${close.min():.2f}  on {df.loc[idx_low,'Date'].date()}")
    print(f"  First Close   : ${close.iloc[0]:.2f}")
    print(f"  Last Close    : ${close.iloc[-1]:.2f}")

    # ── Volume Stats ──────────────────────────────────────────────────────────
    print(f"\n  Volume Statistics:")
    print(f"    Average Volume  : {df['Volume'].mean():>15,.0f}")
    print(f"    Max Volume      : {df['Volume'].max():>15,}")
    print(f"    Min Volume      : {df['Volume'].min():>15,}")

    # ── Year-wise Summary ─────────────────────────────────────────────────────
    print(f"\n  Year-wise Close Price Summary:")
    yearly = df.groupby("Year")["Close"].agg(["min","max","mean"]).round(2)
    yearly.columns = ["Min", "Max", "Mean"]
    print(yearly.to_string())

    # ── Return summary ────────────────────────────────────────────────────────
    df["Daily_Return"] = close.pct_change()
    print(f"\n  Daily Return Stats:")
    print(f"    Mean Return     : {df['Daily_Return'].mean()*100:>8.4f}%")
    print(f"    Std Dev         : {df['Daily_Return'].std()*100:>8.4f}%")
    print(f"    Best Day        : {df['Daily_Return'].max()*100:>8.4f}%  on {df.loc[df['Daily_Return'].idxmax(),'Date'].date()}")
    print(f"    Worst Day       : {df['Daily_Return'].min()*100:>8.4f}%  on {df.loc[df['Daily_Return'].idxmin(),'Date'].date()}")
    print(f"    Positive Days   : {(df['Daily_Return']>0).sum():>8} / {len(df)-1} ({(df['Daily_Return']>0).mean()*100:.1f}%)")

    return {
        "Ticker":         ticker,
        "Start":          str(df["Date"].min().date()),
        "End":            str(df["Date"].max().date()),
        "Trading_Days":   len(df),
        "First_Close":    round(float(close.iloc[0]), 2),
        "Last_Close":     round(float(close.iloc[-1]), 2),
        "All_Time_High":  round(float(close.max()), 2),
        "All_Time_Low":   round(float(close.min()), 2),
        "Mean_Close":     round(float(close.mean()), 2),
        "Std_Close":      round(float(close.std()), 2),
        "Avg_Volume":     int(df["Volume"].mean()),
        "Avg_Daily_Ret%": round(float(df["Daily_Return"].mean())*100, 4),
        "Std_Daily_Ret%": round(float(df["Daily_Return"].std())*100, 4),
        "Positive_Days%": round(float((df["Daily_Return"]>0).mean())*100, 1),
    }


def run_eda():
    """Run EDA on all tickers and save summary CSV."""
    print("\n" + "="*60)
    print("  STEP 3 — EXPLORATORY DATA ANALYSIS (EDA)")
    print("="*60)

    summaries = []
    for ticker in TICKERS:
        path = os.path.join(DATA_DIR, f"{ticker}_clean.csv")
        if not os.path.exists(path):
            print(f"[SKIP] {path} not found.")
            continue
        df  = pd.read_csv(path)
        s   = eda_single(df, ticker)
        summaries.append(s)

    if summaries:
        out = pd.DataFrame(summaries)
        out_path = os.path.join(OUTPUTS_DIR, "eda_summary.csv")
        out.to_csv(out_path, index=False)
        print(f"\n[SAVED] EDA summary → {out_path}")
        print(f"\n  Side-by-Side Comparison:")
        print(out.set_index("Ticker").T.to_string())

    print("\n[DONE] Step 3 complete.")
    return summaries


if __name__ == "__main__":
    run_eda()
