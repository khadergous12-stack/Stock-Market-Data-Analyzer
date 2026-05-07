"""
=============================================================
 STOCK MARKET DATA ANALYZER
 Step 5 — Risk & Volatility Analysis
 Input : data/{TICKER}_indicators.csv
 Output: outputs/risk_summary.csv (printed + saved)
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
TRADING_DAYS = 252
os.makedirs(OUTPUTS_DIR, exist_ok=True)


def risk_analysis(df: pd.DataFrame, ticker: str) -> dict:
    """
    Compute comprehensive risk/return metrics:
        - Total return, annualised return
        - Daily & annual volatility
        - Sharpe ratio (risk-free rate = 0 for simplicity)
        - Maximum drawdown
        - Value at Risk (VaR 95%)
        - Beta vs. buy-and-hold (proxy)
        - Positive/negative day percentages
    """
    df["Date"] = pd.to_datetime(df["Date"])
    dr  = df["Daily_Return"].dropna().astype(float)
    close = df["Close"].astype(float)

    # ── Return Metrics ────────────────────────────────────────────────────────
    total_return   = float((1 + dr).prod() - 1)
    n_years        = len(dr) / TRADING_DAYS
    annual_return  = float((1 + total_return) ** (1 / max(n_years, 0.01)) - 1)

    # ── Volatility ────────────────────────────────────────────────────────────
    daily_vol   = float(dr.std())
    annual_vol  = daily_vol * np.sqrt(TRADING_DAYS)

    # ── Sharpe Ratio (risk-free rate = 0) ─────────────────────────────────────
    sharpe = (dr.mean() / daily_vol * np.sqrt(TRADING_DAYS)) if daily_vol > 0 else 0.0

    # ── Maximum Drawdown ──────────────────────────────────────────────────────
    equity      = (1 + dr).cumprod()
    peak        = equity.cummax()
    drawdown    = (equity / peak - 1)
    max_dd      = float(drawdown.min())
    max_dd_date = df["Date"].iloc[drawdown.idxmin() + 1] if len(drawdown) > 1 else None

    # ── Value at Risk (VaR 95%, Historical) ──────────────────────────────────
    var_95 = float(np.percentile(dr.dropna(), 5))  # 5th percentile

    # ── Streak Analysis ───────────────────────────────────────────────────────
    pos_streak = neg_streak = cur = 0
    for r in dr:
        if r > 0:
            cur = max(cur + 1, 1) if cur >= 0 else 1
            pos_streak = max(pos_streak, cur)
        elif r < 0:
            cur = min(cur - 1, -1) if cur <= 0 else -1
            neg_streak = min(neg_streak, cur)

    # ── Print ─────────────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"  Risk Analysis — {ticker}")
    print(f"{'='*60}")
    print(f"\n  ── Return ──────────────────────────────────────────────")
    print(f"  Total Return          : {total_return*100:>9.2f}%")
    print(f"  Annualised Return     : {annual_return*100:>9.2f}%")
    print(f"  Avg Daily Return      : {dr.mean()*100:>9.4f}%")
    print(f"  Positive Days         : {(dr>0).sum():>9} ({(dr>0).mean()*100:.1f}%)")
    print(f"  Negative Days         : {(dr<0).sum():>9} ({(dr<0).mean()*100:.1f}%)")
    print(f"  Best Single Day       : {dr.max()*100:>9.4f}%")
    print(f"  Worst Single Day      : {dr.min()*100:>9.4f}%")
    print(f"  Longest Win Streak    : {pos_streak:>9} days")
    print(f"  Longest Loss Streak   : {abs(neg_streak):>9} days")
    print(f"\n  ── Risk ────────────────────────────────────────────────")
    print(f"  Daily Volatility      : {daily_vol*100:>9.4f}%")
    print(f"  Annual Volatility     : {annual_vol*100:>9.2f}%")
    print(f"  Sharpe Ratio          : {sharpe:>9.4f}")
    print(f"  Maximum Drawdown      : {max_dd*100:>9.2f}%")
    if max_dd_date is not None:
        print(f"  Max DD Date           : {str(max_dd_date.date()):>9}")
    print(f"  VaR (95%, 1-day)      : {var_95*100:>9.4f}%")
    print(f"    → On 95% of days, loss ≤ {abs(var_95)*100:.2f}%")

    # Interpretation
    print(f"\n  ── Interpretation ──────────────────────────────────────")
    if sharpe > 1.5:
        print(f"  ✅ Sharpe {sharpe:.2f} → Excellent risk-adjusted returns")
    elif sharpe > 0.5:
        print(f"  ⚡ Sharpe {sharpe:.2f} → Moderate risk-adjusted returns")
    else:
        print(f"  ⚠  Sharpe {sharpe:.2f} → Low risk-adjusted returns")

    if abs(max_dd) > 0.40:
        print(f"  ⚠  Max Drawdown {max_dd*100:.1f}% → High historical risk")
    elif abs(max_dd) > 0.20:
        print(f"  ⚡ Max Drawdown {max_dd*100:.1f}% → Moderate historical risk")
    else:
        print(f"  ✅ Max Drawdown {max_dd*100:.1f}% → Contained historical risk")

    return {
        "Ticker":            ticker,
        "Total_Return%":     round(total_return * 100, 2),
        "Annual_Return%":    round(annual_return * 100, 2),
        "Daily_Vol%":        round(daily_vol * 100, 4),
        "Annual_Vol%":       round(annual_vol * 100, 2),
        "Sharpe_Ratio":      round(float(sharpe), 4),
        "Max_Drawdown%":     round(max_dd * 100, 2),
        "VaR_95%":           round(var_95 * 100, 4),
        "Positive_Days%":    round((dr > 0).mean() * 100, 1),
        "Best_Day%":         round(float(dr.max()) * 100, 4),
        "Worst_Day%":        round(float(dr.min()) * 100, 4),
        "Win_Streak_Days":   pos_streak,
        "Loss_Streak_Days":  abs(neg_streak),
    }


def run_risk_analysis():
    """Run risk analysis for all tickers."""
    print("\n" + "="*60)
    print("  STEP 5 — RISK & VOLATILITY ANALYSIS")
    print("="*60)

    results = []
    for ticker in TICKERS:
        path = os.path.join(DATA_DIR, f"{ticker}_indicators.csv")
        if not os.path.exists(path):
            print(f"[SKIP] {path} not found.")
            continue
        df = pd.read_csv(path)
        r  = risk_analysis(df, ticker)
        results.append(r)

    if results:
        rdf = pd.DataFrame(results)
        out_path = os.path.join(OUTPUTS_DIR, "risk_summary.csv")
        rdf.to_csv(out_path, index=False)
        print(f"\n[SAVED] Risk summary → {out_path}")
        print(f"\n  Comparison Table:")
        print(rdf.set_index("Ticker").T.to_string())

    print("\n[DONE] Step 5 complete.")
    return results


if __name__ == "__main__":
    run_risk_analysis()
