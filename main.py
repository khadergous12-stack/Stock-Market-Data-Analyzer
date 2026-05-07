#!/usr/bin/env python3
"""
=============================================================
 STOCK MARKET DATA ANALYZER — MAIN PIPELINE
=============================================================
 USAGE:
   python main.py                     # default: AAPL, MSFT, GOOGL
   python main.py --tickers AAPL TSLA
   python main.py --tickers AAPL --csv data/AAPL.csv
   python main.py --no-charts         # skip chart generation

 WHAT THIS DOES (7 steps):
   Step 1 — Download OHLCV data from Yahoo Finance
   Step 2 — Clean and validate the data
   Step 3 — Exploratory Data Analysis (EDA)
   Step 4 — Compute Moving Averages & Returns
   Step 5 — Risk & Volatility Analysis
   Step 6 — Generate 8 charts per ticker (25 charts total)
   Step 7 — Generate Text & CSV Report

 OUTPUT:
   data/        → raw & cleaned CSVs + indicator CSVs
   outputs/     → 25 PNG charts
   reports/     → stock_analysis_report.txt + risk_return_summary.csv

 DISCLAIMER: Educational purposes only. NOT financial advice.
=============================================================
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(__file__))


def banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║         📈  STOCK MARKET DATA ANALYZER  📈              ║
║                                                          ║
║  Tools  : Python · Pandas · NumPy · Matplotlib · yfinance║
║  Output : Charts · CSV · Text Report                     ║
║                                                          ║
║  ⚠  DISCLAIMER: Educational only. Not financial advice. ║
╚══════════════════════════════════════════════════════════╝
""")


def step_header(n, title):
    print(f"\n{'━'*60}")
    print(f"  ▶  STEP {n}/7 — {title}")
    print(f"{'━'*60}")


def parse_args():
    p = argparse.ArgumentParser(description="Stock Market Data Analyzer")
    p.add_argument("--tickers",   nargs="+", default=["AAPL","MSFT","GOOGL"])
    p.add_argument("--start",     default="2018-01-01")
    p.add_argument("--end",       default="2024-12-31")
    p.add_argument("--csv",       default=None, help="Local CSV for first ticker")
    p.add_argument("--no-charts", action="store_true")
    return p.parse_args()


def main():
    banner()
    args = parse_args()

    # Patch TICKERS list into each step module dynamically
    import src.step1_data_collection as s1
    import src.step2_data_cleaning   as s2
    import src.step3_eda             as s3
    import src.step4_moving_averages as s4
    import src.step5_risk_analysis   as s5
    import src.step6_visualization   as s6
    import src.step7_report          as s7

    tickers = [t.upper() for t in args.tickers]
    for mod in [s1, s2, s3, s4, s5, s6, s7]:
        mod.TICKERS = tickers

    s1.START_DATE = args.start
    s1.END_DATE   = args.end

    # ── Step 1 ────────────────────────────────────────────────────────────────
    step_header(1, "STOCK DATA COLLECTION (Yahoo Finance)")
    s1.collect_all()

    # ── Step 2 ────────────────────────────────────────────────────────────────
    step_header(2, "DATA CLEANING")
    s2.clean_all()

    # ── Step 3 ────────────────────────────────────────────────────────────────
    step_header(3, "EXPLORATORY DATA ANALYSIS")
    s3.run_eda()

    # ── Step 4 ────────────────────────────────────────────────────────────────
    step_header(4, "MOVING AVERAGES & RETURNS CALCULATION")
    s4.compute_all()

    # ── Step 5 ────────────────────────────────────────────────────────────────
    step_header(5, "RISK & VOLATILITY ANALYSIS")
    s5.run_risk_analysis()

    # ── Step 6 ────────────────────────────────────────────────────────────────
    if args.no_charts:
        step_header(6, "VISUALIZATION (SKIPPED — use --no-charts to re-enable)")
    else:
        step_header(6, "VISUALIZATION (8 CHARTS PER TICKER)")
        s6.visualize_all()

    # ── Step 7 ────────────────────────────────────────────────────────────────
    step_header(7, "REPORT GENERATION")
    s7.generate_report()

    # ── Final Summary ─────────────────────────────────────────────────────────
    print(f"""
╔══════════════════════════════════════════════════════════╗
║                ✅  PIPELINE COMPLETE                     ║
╠══════════════════════════════════════════════════════════╣
║  📁 data/       → Raw + Cleaned + Indicator CSVs         ║
║  📊 outputs/    → PNG Charts (8 per ticker + comparison) ║
║  📄 reports/    → .txt Report + .csv Summary             ║
╚══════════════════════════════════════════════════════════╝
  ⚠  This project is for EDUCATIONAL PURPOSES ONLY.
     It does NOT constitute financial advice.
""")


if __name__ == "__main__":
    main()
