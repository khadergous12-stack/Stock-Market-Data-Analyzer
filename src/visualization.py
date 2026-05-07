"""
=============================================================
 STOCK MARKET DATA ANALYZER
 Step 6 — Visualization (8 Charts per ticker)
 Input : data/{TICKER}_indicators.csv
 Output: outputs/{TICKER}_*.png  (8 charts saved)
         outputs/comparison_chart.png
=============================================================
 DISCLAIMER: Educational purposes only. Not financial advice.
=============================================================
"""

import os
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.gridspec as gridspec
import seaborn as sns

DATA_DIR    = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUTS_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
TICKERS     = ["AAPL", "MSFT", "GOOGL"]
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# ── Dark professional theme ───────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor" : "#0d1117",
    "axes.facecolor"   : "#161b22",
    "axes.edgecolor"   : "#30363d",
    "axes.labelcolor"  : "#c9d1d9",
    "xtick.color"      : "#8b949e",
    "ytick.color"      : "#8b949e",
    "text.color"       : "#c9d1d9",
    "grid.color"       : "#21262d",
    "grid.alpha"       : 0.8,
    "lines.linewidth"  : 1.6,
    "font.family"      : "DejaVu Sans",
    "font.size"        : 10,
    "axes.titlesize"   : 13,
    "axes.labelsize"   : 10,
    "legend.fontsize"  : 9,
    "legend.framealpha": 0.2,
    "legend.edgecolor" : "#30363d",
})

C = {
    "price"  : "#58a6ff",
    "sma20"  : "#ffa657",
    "sma50"  : "#ff7b72",
    "sma200" : "#bc8cff",
    "ema20"  : "#3fb950",
    "bb_u"   : "#79c0ff",
    "bb_l"   : "#79c0ff",
    "bb_m"   : "#388bfd",
    "buy"    : "#3fb950",
    "sell"   : "#f85149",
    "vol"    : "#ffa657",
    "return" : "#58a6ff",
    "green"  : "#3fb950",
    "red"    : "#f85149",
    "cum"    : "#3fb950",
    "dd"     : "#f85149",
}


def _fmt_date(ax):
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right", fontsize=8)


def _save(fig, name):
    path = os.path.join(OUTPUTS_DIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  [SAVED] {path}")
    return path


# ─────────────────────────────────────────────────────────────────────────────
# Chart 1 — Closing Price + Volume
# ─────────────────────────────────────────────────────────────────────────────
def chart1_price_volume(df, ticker):
    fig = plt.figure(figsize=(14, 7))
    gs  = gridspec.GridSpec(2, 1, height_ratios=[3, 1], hspace=0.05)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)

    ax1.plot(df["Date"], df["Close"], color=C["price"], lw=1.8, label="Close Price")
    ax1.fill_between(df["Date"], df["Close"], df["Close"].min(), alpha=0.07, color=C["price"])
    ax1.set_ylabel("Price (USD)", color=C["price"])
    ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0f"))
    ax1.set_title(f"{ticker}  —  Closing Price & Volume", pad=15, fontweight="bold")
    ax1.legend(loc="upper left")
    ax1.tick_params(labelbottom=False)

    colors = [C["green"] if r >= 0 else C["red"]
              for r in df["Close"].pct_change().fillna(0)]
    ax2.bar(df["Date"], df["Volume"] / 1e6, color=colors, width=1.5, alpha=0.7)
    ax2.set_ylabel("Vol (M)", fontsize=8)
    _fmt_date(ax2)
    _save(fig, f"{ticker}_01_price_volume.png")


# ─────────────────────────────────────────────────────────────────────────────
# Chart 2 — Price + Moving Averages
# ─────────────────────────────────────────────────────────────────────────────
def chart2_price_sma(df, ticker):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df["Date"], df["Close"],   color=C["price"],  lw=1.8, label="Close")
    ax.plot(df["Date"], df["SMA_20"],  color=C["sma20"],  lw=1.4, ls="--", label="SMA-20")
    ax.plot(df["Date"], df["SMA_50"],  color=C["sma50"],  lw=1.4, ls="-.", label="SMA-50")
    ax.plot(df["Date"], df["SMA_200"], color=C["sma200"], lw=1.2, ls=":",  label="SMA-200")
    ax.plot(df["Date"], df["EMA_20"],  color=C["ema20"],  lw=1.2, alpha=0.7, label="EMA-20")

    # Mark Golden Cross / Death Cross
    gc = df[df["Golden_Cross"] == 1]
    dc = df[df["Death_Cross"] == 1]
    ax.scatter(gc["Date"], gc["Close"], marker="^", color=C["buy"],  s=80, zorder=5, label="Golden Cross ▲")
    ax.scatter(dc["Date"], dc["Close"], marker="v", color=C["sell"], s=80, zorder=5, label="Death Cross ▼")

    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0f"))
    ax.set_title(f"{ticker}  —  Moving Averages + Golden/Death Cross", fontweight="bold", pad=15)
    ax.set_ylabel("Price (USD)")
    ax.legend(ncol=4, loc="upper left")
    _fmt_date(ax)
    _save(fig, f"{ticker}_02_moving_averages.png")


# ─────────────────────────────────────────────────────────────────────────────
# Chart 3 — Bollinger Bands
# ─────────────────────────────────────────────────────────────────────────────
def chart3_bollinger(df, ticker):
    # Compute Bollinger manually from Close + SMA_20
    df = df.copy()
    std = df["Close"].rolling(20).std()
    df["BB_Upper"] = df["SMA_20"] + 2 * std
    df["BB_Lower"] = df["SMA_20"] - 2 * std

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df["Date"], df["Close"],    color=C["price"],  lw=1.8, label="Close")
    ax.plot(df["Date"], df["BB_Upper"], color=C["bb_u"],   lw=1.0, ls="--", alpha=0.8, label="BB Upper")
    ax.plot(df["Date"], df["SMA_20"],   color=C["bb_m"],   lw=1.0, alpha=0.8, label="SMA-20 (Mid)")
    ax.plot(df["Date"], df["BB_Lower"], color=C["bb_l"],   lw=1.0, ls="--", alpha=0.8, label="BB Lower")
    ax.fill_between(df["Date"], df["BB_Upper"], df["BB_Lower"], alpha=0.06, color=C["bb_u"])

    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0f"))
    ax.set_title(f"{ticker}  —  Bollinger Bands (20-day, 2σ)", fontweight="bold", pad=15)
    ax.set_ylabel("Price (USD)")
    ax.legend(ncol=4, loc="upper left")
    _fmt_date(ax)
    _save(fig, f"{ticker}_03_bollinger_bands.png")


# ─────────────────────────────────────────────────────────────────────────────
# Chart 4 — Daily Returns
# ─────────────────────────────────────────────────────────────────────────────
def chart4_daily_returns(df, ticker):
    ret = df["Daily_Return"].dropna() * 100  # percent

    fig = plt.figure(figsize=(14, 7))
    gs  = gridspec.GridSpec(2, 1, height_ratios=[1, 1], hspace=0.4)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])

    # Bar chart of daily returns
    colors = [C["green"] if v >= 0 else C["red"] for v in ret]
    ax1.bar(df["Date"].iloc[1:len(ret)+1], ret, color=colors, width=1.5, alpha=0.8)
    ax1.axhline(0, color="#555", lw=0.8)
    ax1.set_title(f"{ticker}  —  Daily Returns (%)", fontweight="bold")
    ax1.set_ylabel("Return (%)")
    _fmt_date(ax1)

    # Histogram + KDE
    ax2.hist(ret, bins=80, color=C["return"], alpha=0.5, edgecolor="none", density=True, label="Histogram")
    ret.plot.kde(ax=ax2, color=C["sma20"], lw=2, label="KDE")
    ax2.axvline(ret.mean(), color=C["sma50"],  lw=1.5, ls="--", label=f"Mean={ret.mean():.3f}%")
    ax2.axvline(0,          color="#555",       lw=0.8, ls="--")
    ax2.set_title(f"{ticker}  —  Daily Return Distribution", fontweight="bold")
    ax2.set_xlabel("Daily Return (%)")
    ax2.set_ylabel("Density")
    ax2.legend()
    _save(fig, f"{ticker}_04_daily_returns.png")


# ─────────────────────────────────────────────────────────────────────────────
# Chart 5 — Cumulative Returns
# ─────────────────────────────────────────────────────────────────────────────
def chart5_cumulative_return(df, ticker):
    cum = df["Cumulative_Return"].dropna() * 100  # percent
    dates = df["Date"].iloc[len(df) - len(cum):]

    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(dates, cum, color=C["cum"], lw=1.8)
    ax.fill_between(dates, 0, cum, where=(cum >= 0), alpha=0.12, color=C["green"])
    ax.fill_between(dates, 0, cum, where=(cum <  0), alpha=0.12, color=C["red"])
    ax.axhline(0, color="#555", lw=0.8, ls="--")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.set_title(f"{ticker}  —  Cumulative Return (%)", fontweight="bold", pad=15)
    ax.set_ylabel("Cumulative Return (%)")
    _fmt_date(ax)
    _save(fig, f"{ticker}_05_cumulative_return.png")


# ─────────────────────────────────────────────────────────────────────────────
# Chart 6 — Rolling Volatility
# ─────────────────────────────────────────────────────────────────────────────
def chart6_rolling_volatility(df, ticker):
    fig = plt.figure(figsize=(14, 7))
    gs  = gridspec.GridSpec(2, 1, height_ratios=[2, 1], hspace=0.05)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)

    ax1.plot(df["Date"], df["Close"], color=C["price"], lw=1.6, label="Close")
    ax1.set_title(f"{ticker}  —  Price & 20-day Rolling Volatility", fontweight="bold", pad=15)
    ax1.set_ylabel("Price (USD)")
    ax1.yaxis.set_major_formatter(mticker.FormatStrFormatter("$%.0f"))
    ax1.legend(loc="upper left")
    ax1.tick_params(labelbottom=False)

    vol = df["Rolling_Vol_20"].dropna() * 100
    ax2.plot(df["Date"].iloc[len(df)-len(vol):], vol, color=C["vol"], lw=1.4)
    ax2.fill_between(df["Date"].iloc[len(df)-len(vol):], 0, vol, alpha=0.15, color=C["vol"])
    ax2.set_ylabel("Ann. Vol %")
    _fmt_date(ax2)
    _save(fig, f"{ticker}_06_rolling_volatility.png")


# ─────────────────────────────────────────────────────────────────────────────
# Chart 7 — Drawdown
# ─────────────────────────────────────────────────────────────────────────────
def chart7_drawdown(df, ticker):
    dr     = df["Daily_Return"].dropna().astype(float)
    equity = (1 + dr).cumprod()
    dd     = (equity / equity.cummax() - 1) * 100
    dates  = df["Date"].iloc[len(df) - len(dd):]

    fig = plt.figure(figsize=(14, 7))
    gs  = gridspec.GridSpec(2, 1, height_ratios=[2, 1], hspace=0.05)
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)

    ax1.plot(dates, equity.values, color=C["price"], lw=1.6)
    ax1.set_title(f"{ticker}  —  Portfolio Growth & Drawdown", fontweight="bold", pad=15)
    ax1.set_ylabel("Portfolio Value (start=1)")
    ax1.tick_params(labelbottom=False)

    ax2.fill_between(dates, 0, dd.values, color=C["dd"], alpha=0.6)
    ax2.plot(dates, dd.values, color=C["dd"], lw=0.8)
    ax2.axhline(0, color="#555", lw=0.6)
    ax2.set_ylabel("Drawdown %")
    _fmt_date(ax2)
    _save(fig, f"{ticker}_07_drawdown.png")


# ─────────────────────────────────────────────────────────────────────────────
# Chart 8 — Monthly Returns Heatmap
# ─────────────────────────────────────────────────────────────────────────────
def chart8_monthly_heatmap(df, ticker):
    df2 = df[["Date", "Daily_Return"]].copy().dropna()
    df2["Date"] = pd.to_datetime(df2["Date"])
    df2["Year"]  = df2["Date"].dt.year
    df2["Month"] = df2["Date"].dt.month
    monthly = df2.groupby(["Year","Month"])["Daily_Return"].apply(
        lambda x: (1+x).prod() - 1
    ).unstack() * 100

    month_names = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    monthly.columns = [month_names[m-1] for m in monthly.columns]

    fig, ax = plt.subplots(figsize=(14, max(4, len(monthly)*0.55 + 1)))
    sns.heatmap(
        monthly, annot=True, fmt=".1f", linewidths=0.4,
        cmap="RdYlGn", center=0,
        annot_kws={"size": 7.5},
        ax=ax,
        cbar_kws={"shrink": 0.6, "label": "Return %"},
    )
    ax.set_facecolor("#161b22")
    ax.set_title(f"{ticker}  —  Monthly Returns Heatmap (%)", fontweight="bold", pad=15)
    ax.set_xlabel("Month"); ax.set_ylabel("Year")
    plt.xticks(rotation=0); plt.yticks(rotation=0)
    _save(fig, f"{ticker}_08_monthly_heatmap.png")


# ─────────────────────────────────────────────────────────────────────────────
# Comparison Chart — All tickers cumulative return
# ─────────────────────────────────────────────────────────────────────────────
def chart_comparison(all_dfs: dict):
    pal = [C["price"], C["sma20"], C["sma200"], "#bc8cff", "#3fb950"]

    fig, ax = plt.subplots(figsize=(14, 6))
    for i, (ticker, df) in enumerate(all_dfs.items()):
        cum = df["Cumulative_Return"].dropna() * 100
        dates = df["Date"].iloc[len(df)-len(cum):]
        ax.plot(dates, cum, color=pal[i % len(pal)], lw=1.8, label=ticker)

    ax.axhline(0, color="#555", lw=0.8, ls="--")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(decimals=0))
    ax.set_title("Cumulative Return Comparison — AAPL vs MSFT vs GOOGL", fontweight="bold", pad=15)
    ax.set_ylabel("Cumulative Return (%)")
    ax.legend(fontsize=11)
    _fmt_date(ax)
    _save(fig, "comparison_cumulative_return.png")


# ─────────────────────────────────────────────────────────────────────────────
# Run all charts
# ─────────────────────────────────────────────────────────────────────────────
def visualize_all():
    print("\n" + "="*60)
    print("  STEP 6 — VISUALIZATION (8 CHARTS PER TICKER)")
    print("="*60)

    all_dfs = {}
    for ticker in TICKERS:
        path = os.path.join(DATA_DIR, f"{ticker}_indicators.csv")
        if not os.path.exists(path):
            print(f"[SKIP] {path} not found.")
            continue

        df = pd.read_csv(path, parse_dates=["Date"])
        all_dfs[ticker] = df

        print(f"\n  Generating 8 charts for {ticker} ...")
        chart1_price_volume(df, ticker)
        chart2_price_sma(df, ticker)
        chart3_bollinger(df, ticker)
        chart4_daily_returns(df, ticker)
        chart5_cumulative_return(df, ticker)
        chart6_rolling_volatility(df, ticker)
        chart7_drawdown(df, ticker)
        chart8_monthly_heatmap(df, ticker)

    if len(all_dfs) > 1:
        print("\n  Generating comparison chart ...")
        chart_comparison(all_dfs)

    total = len(TICKERS) * 8 + (1 if len(all_dfs) > 1 else 0)
    print(f"\n[DONE] Step 6 complete. {total} charts saved to outputs/ folder.")


if __name__ == "__main__":
    visualize_all()
