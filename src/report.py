"""
=============================================================
 STOCK MARKET DATA ANALYZER
 Step 7 — Report Generation
 Input : outputs/risk_summary.csv + data/{TICKER}_indicators.csv
 Output: reports/stock_analysis_report.txt
         reports/full_data_summary.csv
=============================================================
 DISCLAIMER: Educational purposes only. Not financial advice.
=============================================================
"""

import os
import datetime as dt
import pandas as pd
import numpy as np

DATA_DIR    = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
TICKERS     = ["AAPL", "MSFT", "GOOGL"]
os.makedirs(REPORTS_DIR, exist_ok=True)

DISCLAIMER = """
╔══════════════════════════════════════════════════════════╗
║               ⚠  IMPORTANT DISCLAIMER  ⚠               ║
╠══════════════════════════════════════════════════════════╣
║  This report is generated for EDUCATIONAL PURPOSES ONLY.║
║  It does NOT constitute financial, investment, or        ║
║  trading advice of any kind.                            ║
║  Past performance does NOT guarantee future results.     ║
║  Always consult a SEBI-registered or qualified financial ║
║  advisor before making any investment decisions.         ║
╚══════════════════════════════════════════════════════════╝
"""


def divider(char="─", width=60):
    return char * width


def section(title):
    return f"\n{divider('═')}\n  {title}\n{divider('═')}"


def generate_report():
    print("\n" + "="*60)
    print("  STEP 7 — REPORT GENERATION")
    print("="*60)

    timestamp = dt.datetime.now().strftime("%d %B %Y  %H:%M:%S")
    lines = []

    # ── Title Block ───────────────────────────────────────────────────────────
    lines += [
        "",
        "╔══════════════════════════════════════════════════════════╗",
        "║         STOCK MARKET DATA ANALYZER — FINAL REPORT       ║",
        f"║  Generated : {timestamp:<44}║",
        "║  Tickers   : AAPL (Apple)  |  MSFT (Microsoft)  |  GOOGL║",
        "║  Data From : Yahoo Finance (yfinance)                    ║",
        "║  Period    : 2018-01-01  →  2024-12-31                   ║",
        "╚══════════════════════════════════════════════════════════╝",
        DISCLAIMER,
    ]

    all_risk = []

    for ticker in TICKERS:
        path = os.path.join(DATA_DIR, f"{ticker}_indicators.csv")
        if not os.path.exists(path):
            lines.append(f"\n[MISSING] {ticker} data not found. Run steps 1-5 first.")
            continue

        df = pd.read_csv(path, parse_dates=["Date"])
        close = df["Close"].astype(float)
        dr    = df["Daily_Return"].dropna().astype(float)

        # Re-compute risk metrics for the report
        total_ret   = float((1 + dr).prod() - 1)
        n_years     = len(dr) / 252
        ann_ret     = float((1 + total_ret) ** (1/max(n_years,0.01)) - 1)
        daily_vol   = float(dr.std())
        ann_vol     = daily_vol * np.sqrt(252)
        sharpe      = float(dr.mean() / daily_vol * np.sqrt(252)) if daily_vol > 0 else 0
        equity      = (1 + dr).cumprod()
        max_dd      = float((equity / equity.cummax() - 1).min())
        var95       = float(np.percentile(dr, 5))
        pos_days    = float((dr > 0).mean())
        sma20_last  = df["SMA_20"].dropna().iloc[-1]
        sma50_last  = df["SMA_50"].dropna().iloc[-1]
        signal      = "BUY 🟢" if sma20_last > sma50_last else "SELL 🔴"

        all_risk.append({
            "Ticker": ticker,
            "Last_Close": round(float(close.iloc[-1]), 2),
            "Total_Return%": round(total_ret*100, 2),
            "Annual_Return%": round(ann_ret*100, 2),
            "Annual_Vol%": round(ann_vol*100, 2),
            "Sharpe_Ratio": round(sharpe, 3),
            "Max_DD%": round(max_dd*100, 2),
            "VaR_95%": round(var95*100, 4),
            "Signal": signal.replace("🟢","BUY").replace("🔴","SELL"),
        })

        lines += [
            section(f"📈  {ticker}"),
            "",
            f"  Company      : {'Apple Inc.' if ticker=='AAPL' else 'Microsoft Corp.' if ticker=='MSFT' else 'Alphabet Inc. (Google)'}",
            f"  Exchange     : NASDAQ",
            f"  Data Period  : {df['Date'].min().date()}  →  {df['Date'].max().date()}",
            f"  Trading Days : {len(df):,}",
            "",
            divider(),
            "  PRICE SUMMARY",
            divider(),
            f"  Opening Price (2018)    : ${close.iloc[0]:>10,.2f}",
            f"  Latest Close            : ${close.iloc[-1]:>10,.2f}",
            f"  All-Time High           : ${close.max():>10,.2f}",
            f"  All-Time Low            : ${close.min():>10,.2f}",
            f"  Average Close Price     : ${close.mean():>10,.2f}",
            "",
            divider(),
            "  MOVING AVERAGES (Latest Values)",
            divider(),
            f"  SMA-20  (20-day avg)    : ${df['SMA_20'].dropna().iloc[-1]:>10,.2f}",
            f"  SMA-50  (50-day avg)    : ${df['SMA_50'].dropna().iloc[-1]:>10,.2f}",
            f"  SMA-200 (200-day avg)   : ${df['SMA_200'].dropna().iloc[-1]:>10,.2f}",
            f"  EMA-20  (exp. avg)      : ${df['EMA_20'].dropna().iloc[-1]:>10,.2f}",
            f"  Current Signal          : {signal}",
            f"  Golden Crosses          : {int(df['Golden_Cross'].sum())}",
            f"  Death Crosses           : {int(df['Death_Cross'].sum())}",
            "",
            divider(),
            "  RETURN ANALYSIS",
            divider(),
            f"  Total Return            : {total_ret*100:>9.2f}%",
            f"  Annualised Return       : {ann_ret*100:>9.2f}%",
            f"  Average Daily Return    : {dr.mean()*100:>9.4f}%",
            f"  Best Single Day         : {dr.max()*100:>9.4f}%",
            f"  Worst Single Day        : {dr.min()*100:>9.4f}%",
            f"  Positive Days           : {(dr>0).sum():>9,} ({pos_days*100:.1f}%)",
            f"  Negative Days           : {(dr<0).sum():>9,} ({(1-pos_days)*100:.1f}%)",
            "",
            divider(),
            "  RISK ANALYSIS",
            divider(),
            f"  Daily Volatility        : {daily_vol*100:>9.4f}%",
            f"  Annual Volatility       : {ann_vol*100:>9.2f}%",
            f"  Sharpe Ratio            : {sharpe:>9.4f}",
            f"  Maximum Drawdown        : {max_dd*100:>9.2f}%",
            f"  VaR (95%, 1-day)        : {var95*100:>9.4f}%",
            f"    Interpretation: On 95% of days, daily loss ≤ {abs(var95)*100:.2f}%",
            "",
            divider(),
            "  INSIGHTS & INTERPRETATION",
            divider(),
        ]

        # Smart interpretation
        if sharpe > 1.0:
            lines.append(f"  ✅ Sharpe Ratio {sharpe:.2f} → Good risk-adjusted returns")
        elif sharpe > 0:
            lines.append(f"  ⚡ Sharpe Ratio {sharpe:.2f} → Moderate returns vs. risk")
        else:
            lines.append(f"  ⚠  Sharpe Ratio {sharpe:.2f} → Returns not compensating for risk")

        if ann_ret > ann_vol:
            lines.append(f"  ✅ Return ({ann_ret*100:.1f}%) > Volatility ({ann_vol*100:.1f}%) → Favourable profile")
        else:
            lines.append(f"  ⚠  Return ({ann_ret*100:.1f}%) < Volatility ({ann_vol*100:.1f}%) → High risk for return earned")

        if abs(max_dd) < 0.25:
            lines.append(f"  ✅ Max Drawdown {max_dd*100:.1f}% → Risk well-contained")
        elif abs(max_dd) < 0.40:
            lines.append(f"  ⚡ Max Drawdown {max_dd*100:.1f}% → Significant but recoverable")
        else:
            lines.append(f"  ⚠  Max Drawdown {max_dd*100:.1f}% → High historical risk event")

        if sma20_last > sma50_last:
            lines.append(f"  ✅ SMA-20 > SMA-50 → Short-term momentum is BULLISH")
        else:
            lines.append(f"  ⚠  SMA-20 < SMA-50 → Short-term momentum is BEARISH")

    # ── Comparison Table ──────────────────────────────────────────────────────
    if all_risk:
        rdf = pd.DataFrame(all_risk)
        lines += [
            section("📊  SIDE-BY-SIDE COMPARISON"),
            "",
            rdf.set_index("Ticker").T.to_string(),
            "",
        ]

    # ── Glossary ──────────────────────────────────────────────────────────────
    lines += [
        section("📖  GLOSSARY OF TERMS"),
        "",
        "  SMA      : Simple Moving Average — average of last N closing prices",
        "  EMA      : Exponential Moving Average — recent prices weighted more",
        "  RSI      : Relative Strength Index — momentum oscillator (0-100)",
        "  MACD     : Moving Avg Convergence Divergence — trend/momentum signal",
        "  Sharpe   : (Return - RiskFreeRate) / Volatility — risk-adjusted return",
        "  Max DD   : Maximum Drawdown — largest peak-to-trough portfolio decline",
        "  VaR 95%  : Value at Risk — estimated max daily loss at 95% confidence",
        "  Volatility: Standard deviation of returns (annualised × √252)",
        "  Bollinger: Price envelope ±2 std dev around 20-day SMA",
        "  Golden ↑ : SMA-20 crosses above SMA-50 (bullish signal)",
        "  Death  ↓ : SMA-20 crosses below SMA-50 (bearish signal)",
        "",
        divider("═"),
        DISCLAIMER,
    ]

    # ── Write Report ──────────────────────────────────────────────────────────
    report_text = "\n".join(lines)
    txt_path    = os.path.join(REPORTS_DIR, "stock_analysis_report.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"\n[SAVED] Text report  → {txt_path}")

    # ── CSV Summary ───────────────────────────────────────────────────────────
    if all_risk:
        csv_path = os.path.join(REPORTS_DIR, "risk_return_summary.csv")
        pd.DataFrame(all_risk).to_csv(csv_path, index=False)
        print(f"[SAVED] CSV summary  → {csv_path}")

    print("\n" + "─"*60)
    print(report_text)
    print("\n[DONE] Step 7 complete. Reports saved to reports/ folder.")
    return txt_path


if __name__ == "__main__":
    generate_report()
