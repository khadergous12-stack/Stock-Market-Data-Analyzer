"""
generate_sample_data.py
Generates realistic synthetic OHLCV data for AAPL, MSFT, GOOGL
to simulate Yahoo Finance output when network is unavailable.
Saves to data/{TICKER}_raw.csv
"""

import os, datetime, numpy as np, pandas as pd

SEED = 42
np.random.seed(SEED)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Real-ish starting prices and drift parameters
PARAMS = {
    "AAPL":  {"start": 43.07,  "mu": 0.00095, "sigma": 0.0135, "vol_base": 25e6},
    "MSFT":  {"start": 85.95,  "mu": 0.00110, "sigma": 0.0125, "vol_base": 20e6},
    "GOOGL": {"start": 52.45,  "mu": 0.00090, "sigma": 0.0140, "vol_base": 18e6},
}

# Trading calendar: weekdays only, 2018-01-01 → 2024-12-31
dates = pd.bdate_range(start="2018-01-01", end="2024-12-31")

for ticker, p in PARAMS.items():
    n   = len(dates)
    ret = np.random.normal(p["mu"], p["sigma"], n)

    # Inject a crash period (2020 March) and recovery
    for i, d in enumerate(dates):
        if d >= pd.Timestamp("2020-02-20") and d <= pd.Timestamp("2020-03-23"):
            ret[i] = np.random.normal(-0.025, 0.030)
        elif d >= pd.Timestamp("2020-03-24") and d <= pd.Timestamp("2020-08-01"):
            ret[i] = np.random.normal(0.006, 0.020)
        # 2022 bear market
        elif d >= pd.Timestamp("2022-01-01") and d <= pd.Timestamp("2022-10-01"):
            ret[i] = np.random.normal(-0.003, 0.018)

    close = p["start"] * np.cumprod(1 + ret)

    daily_range_pct = np.abs(np.random.normal(0.018, 0.008, n)).clip(0.003, 0.06)
    high  = close * (1 + daily_range_pct * np.random.uniform(0.3, 0.7, n))
    low   = close * (1 - daily_range_pct * np.random.uniform(0.3, 0.7, n))
    open_ = close * (1 + np.random.normal(0, 0.005, n))
    open_ = np.clip(open_, low, high)

    # Volume: higher on volatile days
    volume = (p["vol_base"] * (1 + 3 * np.abs(ret)) * np.random.uniform(0.7, 1.3, n)).astype(int)

    df = pd.DataFrame({
        "Date":      [d.date() for d in dates],
        "Open":      open_.round(4),
        "High":      high.round(4),
        "Low":       low.round(4),
        "Close":     close.round(4),
        "Adj_Close": close.round(4),   # simplified: adj = close
        "Volume":    volume,
    })

    path = os.path.join(DATA_DIR, f"{ticker}_raw.csv")
    df.to_csv(path, index=False)
    print(f"[GEN] {ticker}: {len(df)} rows  |  ${df['Close'].iloc[0]:.2f} → ${df['Close'].iloc[-1]:.2f}  |  {path}")

print("Sample data generation complete.")
