"""
=============================================================
  STOCK MARKET DATA ANALYZER — STREAMLIT DASHBOARD
  Full-featured interactive dashboard for analyzing stocks
  using yfinance, Plotly, and Pandas.

  DISCLAIMER: For educational purposes only.
              Not financial advice.
=============================================================

INSTALL (run once):
    pip install streamlit plotly yfinance pandas numpy ta

RUN:
    streamlit run dashboard.py
=============================================================
"""

import os
import warnings
import datetime as dt
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import yfinance as yf

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG  (must be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Stock Market Data Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Import fonts */
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] {
      font-family: 'Space Grotesk', sans-serif;
  }

  /* Main background */
  .stApp {
      background: #0a0e1a;
      color: #e2e8f0;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
      background: #0f1629 !important;
      border-right: 1px solid #1e2a45;
  }
  [data-testid="stSidebar"] * {
      color: #cbd5e1 !important;
  }

  /* Metric cards */
  [data-testid="stMetric"] {
      background: #111827;
      border: 1px solid #1e2a45;
      border-radius: 12px;
      padding: 16px 20px;
  }
  [data-testid="stMetricLabel"] {
      font-size: 11px !important;
      font-weight: 600 !important;
      letter-spacing: 0.08em !important;
      text-transform: uppercase !important;
      color: #64748b !important;
  }
  [data-testid="stMetricValue"] {
      font-size: 24px !important;
      font-weight: 700 !important;
      font-family: 'JetBrains Mono', monospace !important;
      color: #f1f5f9 !important;
  }
  [data-testid="stMetricDelta"] {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 13px !important;
  }

  /* Header */
  .hero-header {
      background: linear-gradient(135deg, #0f1629 0%, #1a2744 50%, #0f1629 100%);
      border: 1px solid #1e3a5f;
      border-radius: 16px;
      padding: 28px 36px;
      margin-bottom: 24px;
      position: relative;
      overflow: hidden;
  }
  .hero-header::before {
      content: '';
      position: absolute;
      top: -50%;
      right: -10%;
      width: 400px;
      height: 400px;
      background: radial-gradient(circle, rgba(59,130,246,0.08) 0%, transparent 70%);
  }
  .hero-title {
      font-size: 28px;
      font-weight: 700;
      color: #f1f5f9;
      margin: 0 0 6px 0;
      letter-spacing: -0.02em;
  }
  .hero-sub {
      font-size: 14px;
      color: #64748b;
      margin: 0;
  }
  .hero-badge {
      display: inline-block;
      background: rgba(59,130,246,0.15);
      border: 1px solid rgba(59,130,246,0.3);
      color: #60a5fa;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.1em;
      padding: 3px 10px;
      border-radius: 20px;
      margin-bottom: 10px;
  }

  /* Section headers */
  .section-header {
      font-size: 13px;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: #3b82f6;
      margin: 24px 0 12px 0;
      padding-bottom: 8px;
      border-bottom: 1px solid #1e2a45;
  }

  /* Signal badge */
  .signal-buy {
      background: rgba(16,185,129,0.15);
      border: 1px solid rgba(16,185,129,0.4);
      color: #10b981;
      padding: 4px 14px;
      border-radius: 20px;
      font-weight: 700;
      font-size: 13px;
      letter-spacing: 0.05em;
  }
  .signal-sell {
      background: rgba(239,68,68,0.15);
      border: 1px solid rgba(239,68,68,0.4);
      color: #ef4444;
      padding: 4px 14px;
      border-radius: 20px;
      font-weight: 700;
      font-size: 13px;
      letter-spacing: 0.05em;
  }
  .signal-hold {
      background: rgba(245,158,11,0.15);
      border: 1px solid rgba(245,158,11,0.4);
      color: #f59e0b;
      padding: 4px 14px;
      border-radius: 20px;
      font-weight: 700;
      font-size: 13px;
      letter-spacing: 0.05em;
  }

  /* Divider */
  hr { border-color: #1e2a45 !important; }

  /* Tab styling */
  .stTabs [data-baseweb="tab-list"] {
      background: #0f1629;
      border-bottom: 1px solid #1e2a45;
      gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
      background: transparent;
      border-radius: 8px 8px 0 0;
      color: #64748b;
      font-weight: 500;
      font-size: 13px;
      padding: 10px 20px;
  }
  .stTabs [aria-selected="true"] {
      background: #1e2a45 !important;
      color: #60a5fa !important;
  }

  /* Dataframe */
  [data-testid="stDataFrame"] {
      border: 1px solid #1e2a45;
      border-radius: 12px;
  }

  /* Disclaimer */
  .disclaimer {
      background: rgba(245,158,11,0.08);
      border: 1px solid rgba(245,158,11,0.25);
      border-radius: 10px;
      padding: 12px 16px;
      font-size: 12px;
      color: #92400e;
      color: #fbbf24;
      margin-top: 20px;
  }

  /* Insight boxes */
  .insight-positive {
      background: rgba(16,185,129,0.08);
      border-left: 3px solid #10b981;
      padding: 10px 14px;
      border-radius: 0 8px 8px 0;
      font-size: 13px;
      color: #a7f3d0;
      margin: 6px 0;
  }
  .insight-negative {
      background: rgba(239,68,68,0.08);
      border-left: 3px solid #ef4444;
      padding: 10px 14px;
      border-radius: 0 8px 8px 0;
      font-size: 13px;
      color: #fca5a5;
      margin: 6px 0;
  }
  .insight-neutral {
      background: rgba(59,130,246,0.08);
      border-left: 3px solid #3b82f6;
      padding: 10px 14px;
      border-radius: 0 8px 8px 0;
      font-size: 13px;
      color: #93c5fd;
      margin: 6px 0;
  }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  PLOTLY THEME
# ─────────────────────────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font=dict(family="Space Grotesk, sans-serif", color="#94a3b8", size=12),
    xaxis=dict(gridcolor="#1e2a45", zeroline=False, showgrid=True),
    yaxis=dict(gridcolor="#1e2a45", zeroline=False, showgrid=True),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1e2a45", borderwidth=1),
    margin=dict(l=40, r=20, t=40, b=40),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#1e2a45", font_size=12),
)
COLORS = {
    "close":     "#60a5fa",
    "sma20":     "#f59e0b",
    "sma50":     "#10b981",
    "sma200":    "#f472b6",
    "ema20":     "#a78bfa",
    "volume":    "#1e3a5f",
    "bb_upper":  "#94a3b8",
    "bb_lower":  "#94a3b8",
    "bb_band":   "rgba(148,163,184,0.06)",
    "green":     "#10b981",
    "red":       "#ef4444",
    "yellow":    "#f59e0b",
    "blue":      "#3b82f6",
}
TICKERS_DEFAULT = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"]

# ─────────────────────────────────────────────────────────────────────────────
#  DATA LOADING & COMPUTATION
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def load_data(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Fetch OHLCV from Yahoo Finance and compute all indicators."""
    df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)
    if df.empty:
        return pd.DataFrame()

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.rename(columns={"Adj Close": "Adj_Close"})
    df = df[["Date", "Open", "High", "Low", "Close", "Adj_Close", "Volume"]].copy()
    df = df.sort_values("Date").reset_index(drop=True)

    # Clean
    df = df.drop_duplicates(subset="Date")
    for col in ["Open", "High", "Low", "Close", "Adj_Close"]:
        df[col] = df[col].ffill().bfill().astype(float)
    df["Volume"] = df["Volume"].fillna(0).astype(int)
    df = df[df["Close"] > 0].reset_index(drop=True)

    close = df["Close"]

    # Moving averages
    df["SMA_20"]  = close.rolling(20).mean().round(4)
    df["SMA_50"]  = close.rolling(50).mean().round(4)
    df["SMA_200"] = close.rolling(200).mean().round(4)
    df["EMA_20"]  = close.ewm(span=20, adjust=False).mean().round(4)

    # Bollinger Bands (20-day, 2σ)
    df["BB_Mid"]   = close.rolling(20).mean()
    df["BB_Std"]   = close.rolling(20).std()
    df["BB_Upper"] = (df["BB_Mid"] + 2 * df["BB_Std"]).round(4)
    df["BB_Lower"] = (df["BB_Mid"] - 2 * df["BB_Std"]).round(4)
    df["BB_Mid"]   = df["BB_Mid"].round(4)

    # Returns
    df["Daily_Return"]      = close.pct_change().round(6)
    df["Log_Return"]        = np.log(close / close.shift(1)).round(6)
    df["Cumulative_Return"] = ((1 + df["Daily_Return"]).cumprod() - 1).round(6)

    # Rolling Volatility (annualised)
    df["Rolling_Vol_20"] = (df["Daily_Return"].rolling(20).std() * np.sqrt(252)).round(6)

    # RSI (14-day)
    delta    = close.diff()
    gain     = delta.clip(lower=0)
    loss     = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=13, adjust=False).mean()
    avg_loss = loss.ewm(com=13, adjust=False).mean()
    rs       = avg_gain / avg_loss.replace(0, np.nan)
    df["RSI_14"] = (100 - (100 / (1 + rs))).round(2)

    # MACD (12-26-9)
    ema12        = close.ewm(span=12, adjust=False).mean()
    ema26        = close.ewm(span=26, adjust=False).mean()
    df["MACD"]         = (ema12 - ema26).round(4)
    df["MACD_Signal"]  = df["MACD"].ewm(span=9, adjust=False).mean().round(4)
    df["MACD_Hist"]    = (df["MACD"] - df["MACD_Signal"]).round(4)

    # Signals
    df["Signal"] = np.where(df["SMA_20"] > df["SMA_50"], "BUY", "SELL")
    prev_above        = df["SMA_20"].shift(1) > df["SMA_50"].shift(1)
    curr_above        = df["SMA_20"] > df["SMA_50"]
    df["Golden_Cross"] = ((~prev_above) & curr_above).astype(int)
    df["Death_Cross"]  = (prev_above & (~curr_above)).astype(int)

    # Helper date columns
    df["Year"]  = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month

    return df


def compute_risk_metrics(df: pd.DataFrame) -> dict:
    dr    = df["Daily_Return"].dropna()
    close = df["Close"].astype(float)

    total_return  = float((1 + dr).prod() - 1)
    n_years       = len(dr) / 252
    annual_return = float((1 + total_return) ** (1 / max(n_years, 0.01)) - 1)
    daily_vol     = float(dr.std())
    annual_vol    = daily_vol * np.sqrt(252)
    sharpe        = float(dr.mean() / daily_vol * np.sqrt(252)) if daily_vol > 0 else 0.0

    equity  = (1 + dr).cumprod()
    peak    = equity.cummax()
    dd      = (equity / peak - 1)
    max_dd  = float(dd.min())
    var_95  = float(np.percentile(dr.dropna(), 5))
    beta    = float(dr.std() * np.sqrt(252))  # simplified proxy

    return {
        "total_return":  total_return,
        "annual_return": annual_return,
        "daily_vol":     daily_vol,
        "annual_vol":    annual_vol,
        "sharpe":        sharpe,
        "max_dd":        max_dd,
        "var_95":        var_95,
        "pos_days_pct":  float((dr > 0).mean()),
        "best_day":      float(dr.max()),
        "worst_day":     float(dr.min()),
        "avg_return":    float(dr.mean()),
        "drawdown_series": dd,
        "equity_curve":    equity,
    }


# ─────────────────────────────────────────────────────────────────────────────
#  CHART BUILDERS
# ─────────────────────────────────────────────────────────────────────────────
def fig_price_volume(df, ticker, show_bb=True):
    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        row_heights=[0.75, 0.25], vertical_spacing=0.03,
    )
    # Candlestick
    fig.add_trace(go.Candlestick(
        x=df["Date"], open=df["Open"], high=df["High"],
        low=df["Low"],  close=df["Close"],
        name="OHLC",
        increasing_line_color=COLORS["green"],
        decreasing_line_color=COLORS["red"],
        increasing_fillcolor=COLORS["green"],
        decreasing_fillcolor=COLORS["red"],
    ), row=1, col=1)
    # Moving averages
    for col, clr, name in [
        ("SMA_20",  COLORS["sma20"],  "SMA 20"),
        ("SMA_50",  COLORS["sma50"],  "SMA 50"),
        ("SMA_200", COLORS["sma200"], "SMA 200"),
    ]:
        fig.add_trace(go.Scatter(
            x=df["Date"], y=df[col], name=name,
            line=dict(color=clr, width=1.5),
        ), row=1, col=1)
    # Bollinger Bands
    if show_bb:
        fig.add_trace(go.Scatter(
            x=df["Date"], y=df["BB_Upper"], name="BB Upper",
            line=dict(color=COLORS["bb_upper"], width=1, dash="dot"),
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df["Date"], y=df["BB_Lower"], name="BB Lower",
            line=dict(color=COLORS["bb_lower"], width=1, dash="dot"),
            fill="tonexty", fillcolor=COLORS["bb_band"],
        ), row=1, col=1)
    # Volume
    colors = [COLORS["green"] if r >= 0 else COLORS["red"]
              for r in df["Daily_Return"].fillna(0)]
    fig.add_trace(go.Bar(
        x=df["Date"], y=df["Volume"], name="Volume",
        marker_color=colors, opacity=0.7,
    ), row=2, col=1)

    fig.update_layout(
        title=f"{ticker} — Price, Moving Averages & Volume",
        xaxis_rangeslider_visible=False,
        height=520,
        **PLOT_LAYOUT,
    )
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    return fig


def fig_returns_distribution(df, ticker):
    dr = df["Daily_Return"].dropna() * 100
    var95 = np.percentile(dr, 5)

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=dr, nbinsx=80, name="Daily Return",
        marker_color=COLORS["blue"], opacity=0.75,
        histnorm="probability density",
    ))
    fig.add_vline(x=var95, line_dash="dash", line_color=COLORS["red"],
                  annotation_text=f"VaR 95%: {var95:.2f}%",
                  annotation_font_color=COLORS["red"])
    fig.add_vline(x=float(dr.mean()), line_dash="dot", line_color=COLORS["green"],
                  annotation_text=f"Mean: {dr.mean():.3f}%",
                  annotation_font_color=COLORS["green"])
    fig.update_layout(
        title=f"{ticker} — Daily Returns Distribution",
        xaxis_title="Daily Return (%)", yaxis_title="Density",
        height=380, **PLOT_LAYOUT,
    )
    return fig


def fig_cumulative_return(df, ticker):
    cr = df[["Date", "Cumulative_Return"]].dropna().copy()
    cr["Cumulative_Return"] *= 100

    fig = go.Figure()
    # Fill area
    fig.add_trace(go.Scatter(
        x=cr["Date"], y=cr["Cumulative_Return"],
        name="Cumulative Return",
        fill="tozeroy",
        fillcolor="rgba(59,130,246,0.12)",
        line=dict(color=COLORS["close"], width=2),
    ))
    fig.add_hline(y=0, line_dash="solid", line_color="#1e2a45")
    fig.update_layout(
        title=f"{ticker} — Cumulative Return (%)",
        xaxis_title="Date", yaxis_title="Return (%)",
        height=350, **PLOT_LAYOUT,
    )
    return fig


def fig_rsi(df, ticker):
    rsi = df[["Date", "RSI_14"]].dropna()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rsi["Date"], y=rsi["RSI_14"], name="RSI 14",
        line=dict(color=COLORS["yellow"], width=1.8),
    ))
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(239,68,68,0.07)",
                  line_width=0, annotation_text="Overbought (>70)",
                  annotation_font_color="#ef4444")
    fig.add_hrect(y0=0, y1=30, fillcolor="rgba(16,185,129,0.07)",
                  line_width=0, annotation_text="Oversold (<30)",
                  annotation_font_color="#10b981")
    fig.add_hline(y=70, line_dash="dash", line_color="#ef4444", line_width=1)
    fig.add_hline(y=30, line_dash="dash", line_color="#10b981", line_width=1)
    fig.update_layout(title=f"{ticker} — RSI (14)", height=300, **PLOT_LAYOUT)
    fig.update_yaxes(range=[0, 100])
    return fig


def fig_macd(df, ticker):
    d = df[["Date", "MACD", "MACD_Signal", "MACD_Hist"]].dropna()
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.6, 0.4], vertical_spacing=0.04)
    fig.add_trace(go.Scatter(x=d["Date"], y=d["MACD"],
                             name="MACD", line=dict(color=COLORS["blue"], width=1.8)),
                  row=1, col=1)
    fig.add_trace(go.Scatter(x=d["Date"], y=d["MACD_Signal"],
                             name="Signal", line=dict(color=COLORS["yellow"], width=1.8)),
                  row=1, col=1)
    colors = [COLORS["green"] if v >= 0 else COLORS["red"]
              for v in d["MACD_Hist"]]
    fig.add_trace(go.Bar(x=d["Date"], y=d["MACD_Hist"], name="Histogram",
                         marker_color=colors, opacity=0.8),
                  row=2, col=1)
    fig.update_layout(title=f"{ticker} — MACD (12-26-9)",
                      height=380, **PLOT_LAYOUT)
    return fig


def fig_drawdown(df, ticker, metrics):
    dd = metrics["drawdown_series"]
    dates = df["Date"].iloc[1:].values if len(df) - 1 == len(dd) else df["Date"].values
    dd_pct = dd.values * 100

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=dd_pct, name="Drawdown",
        fill="tozeroy",
        fillcolor="rgba(239,68,68,0.12)",
        line=dict(color=COLORS["red"], width=1.5),
    ))
    fig.add_hline(y=float(dd_pct.min()), line_dash="dash",
                  line_color=COLORS["yellow"],
                  annotation_text=f"Max DD: {dd_pct.min():.1f}%",
                  annotation_font_color=COLORS["yellow"])
    fig.update_layout(title=f"{ticker} — Drawdown from Peak (%)",
                      yaxis_title="Drawdown (%)", height=300, **PLOT_LAYOUT)
    return fig


def fig_volatility(df, ticker):
    vol = df[["Date", "Rolling_Vol_20"]].dropna().copy()
    vol["Rolling_Vol_20"] *= 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=vol["Date"], y=vol["Rolling_Vol_20"], name="20d Vol (Ann.)",
        fill="tozeroy",
        fillcolor="rgba(167,139,250,0.1)",
        line=dict(color=COLORS["ema20"], width=1.8),
    ))
    fig.update_layout(title=f"{ticker} — Rolling 20-Day Annualised Volatility (%)",
                      yaxis_title="Volatility (%)", height=300, **PLOT_LAYOUT)
    return fig


def fig_monthly_heatmap(df, ticker):
    d = df.copy()
    d["Month_Name"] = d["Date"].dt.strftime("%b")
    monthly = (
        d.groupby(["Year", "Month"])["Daily_Return"]
         .apply(lambda r: float((1 + r).prod() - 1) * 100)
         .reset_index()
    )
    monthly["Month_Name"] = pd.to_datetime(
        monthly["Month"].astype(str), format="%m"
    ).dt.strftime("%b")

    pivot = monthly.pivot(index="Year", columns="Month_Name", values="Daily_Return")
    month_order = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    pivot = pivot.reindex(columns=[m for m in month_order if m in pivot.columns])

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[[0, "#7f1d1d"], [0.5, "#111827"], [1, "#064e3b"]],
        zmid=0,
        text=pivot.values.round(1),
        texttemplate="%{text}%",
        textfont=dict(size=11),
        colorbar=dict(title="Return %"),
    ))
    fig.update_layout(
        title=f"{ticker} — Monthly Return Heatmap (%)",
        xaxis_title="Month", yaxis_title="Year",
        height=380, **PLOT_LAYOUT,
    )
    return fig


def fig_comparison(dfs: dict):
    """Cumulative returns comparison across multiple tickers."""
    fig = go.Figure()
    palette = ["#60a5fa", "#10b981", "#f59e0b", "#f472b6", "#a78bfa", "#34d399"]
    for i, (t, df) in enumerate(dfs.items()):
        cr = df[["Date", "Cumulative_Return"]].dropna().copy()
        cr["Cumulative_Return"] *= 100
        fig.add_trace(go.Scatter(
            x=cr["Date"], y=cr["Cumulative_Return"], name=t,
            line=dict(color=palette[i % len(palette)], width=2),
        ))
    fig.add_hline(y=0, line_dash="solid", line_color="#1e2a45")
    fig.update_layout(
        title="Cumulative Return Comparison (%)",
        xaxis_title="Date", yaxis_title="Return (%)",
        height=420, **PLOT_LAYOUT,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-size:20px;font-weight:700;color:#f1f5f9;margin-bottom:4px">📈 Stock Analyzer</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:11px;color:#64748b;margin-bottom:20px">Educational Project · Not Financial Advice</p>', unsafe_allow_html=True)
    st.divider()

    st.markdown('<p class="section-header">⚙ Configuration</p>', unsafe_allow_html=True)

    ticker_input = st.text_input(
        "Primary Ticker",
        value="AAPL",
        placeholder="e.g. AAPL, MSFT, TSLA",
    ).upper().strip()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=dt.date(2020, 1, 1),
                                   min_value=dt.date(2000, 1, 1))
    with col2:
        end_date = st.date_input("End Date", value=dt.date.today())

    st.divider()
    st.markdown('<p class="section-header">🔍 Overlays</p>', unsafe_allow_html=True)
    show_sma20  = st.checkbox("SMA 20",  value=True)
    show_sma50  = st.checkbox("SMA 50",  value=True)
    show_sma200 = st.checkbox("SMA 200", value=True)
    show_bb     = st.checkbox("Bollinger Bands", value=True)

    st.divider()
    st.markdown('<p class="section-header">📊 Comparison</p>', unsafe_allow_html=True)
    compare_tickers = st.multiselect(
        "Add tickers to compare",
        options=TICKERS_DEFAULT,
        default=["MSFT", "GOOGL"],
        max_selections=5,
    )

    st.divider()
    st.markdown('<p class="section-header">💡 Quick Links</p>', unsafe_allow_html=True)
    for t in TICKERS_DEFAULT[:5]:
        if st.button(f"→ {t}", key=f"quick_{t}", use_container_width=True):
            ticker_input = t

    st.divider()
    st.markdown('<div class="disclaimer">⚠️ <strong>Disclaimer:</strong> This tool is for educational purposes only. Charts and analysis do not constitute financial advice.</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
  <span class="hero-badge">EDUCATIONAL PROJECT</span>
  <h1 class="hero-title">📈 Stock Market Data Analyzer</h1>
  <p class="hero-sub">Technical analysis · Risk metrics · Backtesting signals · Multi-ticker comparison</p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
with st.spinner(f"Fetching {ticker_input} data from Yahoo Finance…"):
    df = load_data(ticker_input, str(start_date), str(end_date))

if df.empty:
    st.error(f"❌ No data found for **{ticker_input}**. Please check the ticker symbol and date range.")
    st.stop()

metrics = compute_risk_metrics(df)
latest  = df.iloc[-1]
prev    = df.iloc[-2]
info    = yf.Ticker(ticker_input).info

company_name = info.get("longName", ticker_input)
sector       = info.get("sector", "—")
industry     = info.get("industry", "—")
mkt_cap      = info.get("marketCap", 0)
pe_ratio     = info.get("trailingPE", None)

# ─────────────────────────────────────────────────────────────────────────────
#  TOP INFO ROW
# ─────────────────────────────────────────────────────────────────────────────
price_chg     = float(latest["Close"] - prev["Close"])
price_chg_pct = float(price_chg / prev["Close"] * 100)
signal_now    = latest["Signal"]
rsi_now       = latest["RSI_14"] if not np.isnan(latest["RSI_14"]) else 0

signal_html = (
    f'<span class="signal-buy">{signal_now}</span>'   if signal_now == "BUY" else
    f'<span class="signal-sell">{signal_now}</span>'  if signal_now == "SELL" else
    f'<span class="signal-hold">{signal_now}</span>'
)

st.markdown(f"""
<div style="background:#111827;border:1px solid #1e2a45;border-radius:12px;padding:16px 24px;margin-bottom:20px;display:flex;align-items:center;gap:32px;flex-wrap:wrap;">
  <div>
    <p style="font-size:12px;color:#64748b;margin:0;letter-spacing:0.08em;text-transform:uppercase">Company</p>
    <p style="font-size:18px;font-weight:700;color:#f1f5f9;margin:2px 0">{company_name}</p>
    <p style="font-size:12px;color:#64748b;margin:0">{sector} · {industry}</p>
  </div>
  <div style="border-left:1px solid #1e2a45;height:50px;"></div>
  <div>
    <p style="font-size:12px;color:#64748b;margin:0;letter-spacing:0.08em;text-transform:uppercase">Last Close</p>
    <p style="font-size:24px;font-weight:700;font-family:'JetBrains Mono',monospace;color:#f1f5f9;margin:2px 0">${latest['Close']:.2f}</p>
    <p style="font-size:13px;color:{'#10b981' if price_chg >= 0 else '#ef4444'};margin:0;font-family:'JetBrains Mono',monospace">{'▲' if price_chg >= 0 else '▼'} ${abs(price_chg):.2f} ({price_chg_pct:+.2f}%)</p>
  </div>
  <div style="border-left:1px solid #1e2a45;height:50px;"></div>
  <div>
    <p style="font-size:12px;color:#64748b;margin:0;letter-spacing:0.08em;text-transform:uppercase">Signal (SMA Cross)</p>
    <div style="margin-top:6px">{signal_html}</div>
  </div>
  <div style="border-left:1px solid #1e2a45;height:50px;"></div>
  <div>
    <p style="font-size:12px;color:#64748b;margin:0;letter-spacing:0.08em;text-transform:uppercase">RSI (14)</p>
    <p style="font-size:20px;font-weight:700;font-family:'JetBrains Mono',monospace;color:{'#ef4444' if rsi_now > 70 else '#10b981' if rsi_now < 30 else '#f1f5f9'};margin:2px 0">{rsi_now:.1f}</p>
    <p style="font-size:12px;color:#64748b;margin:0">{'🔴 Overbought' if rsi_now > 70 else '🟢 Oversold' if rsi_now < 30 else '⚪ Neutral'}</p>
  </div>
  <div style="border-left:1px solid #1e2a45;height:50px;"></div>
  <div>
    <p style="font-size:12px;color:#64748b;margin:0;letter-spacing:0.08em;text-transform:uppercase">Market Cap</p>
    <p style="font-size:18px;font-weight:700;color:#f1f5f9;margin:2px 0">{'${:,.0f}B'.format(mkt_cap/1e9) if mkt_cap else '—'}</p>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  KEY METRICS ROW
# ─────────────────────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    st.metric("Total Return", f"{metrics['total_return']*100:.1f}%",
              delta=f"{metrics['annual_return']*100:.1f}% / yr")
with c2:
    st.metric("Sharpe Ratio", f"{metrics['sharpe']:.2f}",
              delta="Good" if metrics['sharpe'] > 1.0 else "Fair" if metrics['sharpe'] > 0.5 else "Weak")
with c3:
    st.metric("Annual Volatility", f"{metrics['annual_vol']*100:.1f}%",
              delta=f"Daily: {metrics['daily_vol']*100:.2f}%")
with c4:
    st.metric("Max Drawdown", f"{metrics['max_dd']*100:.1f}%",
              delta="High Risk" if abs(metrics['max_dd']) > 0.4 else "Moderate",
              delta_color="inverse")
with c5:
    st.metric("VaR (95%, 1d)", f"{metrics['var_95']*100:.2f}%",
              delta="Max daily loss (95%)")
with c6:
    st.metric("Win Rate", f"{metrics['pos_days_pct']*100:.1f}%",
              delta=f"Best: {metrics['best_day']*100:.2f}%")


# ─────────────────────────────────────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Price & MAs",
    "📉 Returns & Risk",
    "🔬 Indicators",
    "🗓 Monthly Heatmap",
    "⚖️ Compare",
    "📋 Raw Data",
    "💡 Insights",
])

# ─────────── TAB 1: Price & Moving Averages ───────────────────────────────────
with tab1:
    st.plotly_chart(fig_price_volume(df, ticker_input, show_bb), use_container_width=True)

    gc_count = int(df["Golden_Cross"].sum())
    dc_count = int(df["Death_Cross"].sum())
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Golden Crosses", gc_count, help="SMA20 crossed above SMA50")
    with c2:
        st.metric("Death Crosses", dc_count, help="SMA20 crossed below SMA50")
    with c3:
        days_on_buy = int((df["Signal"] == "BUY").sum())
        pct_buy     = days_on_buy / len(df) * 100
        st.metric("Days on BUY Signal", f"{pct_buy:.1f}%",
                  delta=f"{days_on_buy} trading days")

    st.markdown('<p class="section-header">Latest Moving Average Values</p>', unsafe_allow_html=True)
    ma_data = pd.DataFrame({
        "Indicator": ["SMA 20", "SMA 50", "SMA 200", "EMA 20"],
        "Value": [
            f"${df['SMA_20'].dropna().iloc[-1]:.2f}",
            f"${df['SMA_50'].dropna().iloc[-1]:.2f}",
            f"${df['SMA_200'].dropna().iloc[-1]:.2f}",
            f"${df['EMA_20'].dropna().iloc[-1]:.2f}",
        ],
        "vs Close": [
            f"{'↑' if df['SMA_20'].dropna().iloc[-1] < latest['Close'] else '↓'} {abs(latest['Close'] - df['SMA_20'].dropna().iloc[-1]):.2f}",
            f"{'↑' if df['SMA_50'].dropna().iloc[-1] < latest['Close'] else '↓'} {abs(latest['Close'] - df['SMA_50'].dropna().iloc[-1]):.2f}",
            f"{'↑' if df['SMA_200'].dropna().iloc[-1] < latest['Close'] else '↓'} {abs(latest['Close'] - df['SMA_200'].dropna().iloc[-1]):.2f}",
            f"{'↑' if df['EMA_20'].dropna().iloc[-1] < latest['Close'] else '↓'} {abs(latest['Close'] - df['EMA_20'].dropna().iloc[-1]):.2f}",
        ],
    })
    st.dataframe(ma_data, use_container_width=True, hide_index=True)



    # ── FOOTER ────────────────────────────────────────────────────────────────
    st.markdown("""
<style>
  @keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position: 400px 0; }
  }
  .footer-wrap {
    background: linear-gradient(135deg, #0f1629 0%, #1a2744 50%, #0f1629 100%);
    border: 1px solid #1e3a5f;
    border-radius: 18px;
    padding: 36px 40px 28px 40px;
    text-align: center;
    margin-top: 32px;
    position: relative;
    overflow: hidden;
  }
  .footer-wrap::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(59,130,246,0.09) 0%, transparent 70%);
    pointer-events: none;
  }
  .footer-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 900;
    letter-spacing: -0.03em;
    background: linear-gradient(90deg, #60a5fa 0%, #a78bfa 35%, #f472b6 65%, #60a5fa 100%);
    background-size: 400px 100%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
    margin: 0 0 12px 0;
    display: block;
  }
  .footer-stack {
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: #94a3b8;
    margin: 0 0 22px 0;
  }
  .footer-stack span {
    color: #60a5fa;
    margin: 0 5px;
  }
  .footer-disclaimer {
    display: inline-block;
    background: rgba(245,158,11,0.1);
    border: 2px solid rgba(245,158,11,0.4);
    border-radius: 40px;
    padding: 10px 28px;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 15px;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: #fbbf24;
    text-transform: uppercase;
    margin-bottom: 18px;
    display: block;
  }
  .footer-made {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 13px;
    font-weight: 500;
    color: #334155;
    margin-top: 14px;
  }
  .footer-dots {
    display: flex;
    justify-content: center;
    gap: 8px;
    margin-bottom: 20px;
  }
  .footer-dot { width: 7px; height: 7px; border-radius: 50%; }
</style>
<div class="footer-wrap">
  <div class="footer-dots">
    <div class="footer-dot" style="background:#60a5fa;opacity:0.9;"></div>
    <div class="footer-dot" style="background:#a78bfa;opacity:0.9;"></div>
    <div class="footer-dot" style="background:#f472b6;opacity:0.9;"></div>
    <div class="footer-dot" style="background:#34d399;opacity:0.9;"></div>
    <div class="footer-dot" style="background:#f59e0b;opacity:0.9;"></div>
  </div>
  <span class="footer-title">📈 Stock Market Data Analyzer</span>
  <p class="footer-stack">
    Built with
    <span>Python</span>·
    <span>Streamlit</span>·
    <span>Plotly</span>·
    <span>yfinance</span>·
    <span>Pandas</span>·
    <span>NumPy</span>
  </p>
  <span class="footer-disclaimer">
    ⚠️ &nbsp; Educational Project Only &nbsp;·&nbsp; Not Financial Advice &nbsp;·&nbsp; Data from Yahoo Finance
  </span>
</div>
""", unsafe_allow_html=True)
# ─────────── TAB 2: Returns & Risk ───────────────────────────────────────────
with tab2:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.plotly_chart(fig_cumulative_return(df, ticker_input), use_container_width=True)
    with col2:
        st.plotly_chart(fig_returns_distribution(df, ticker_input), use_container_width=True)

    st.plotly_chart(fig_drawdown(df, ticker_input, metrics), use_container_width=True)
    st.plotly_chart(fig_volatility(df, ticker_input), use_container_width=True)

    st.markdown('<p class="section-header">Risk Summary Table</p>', unsafe_allow_html=True)
    risk_df = pd.DataFrame([{
        "Metric":        m,
        "Value":         v
    } for m, v in {
        "Total Return":          f"{metrics['total_return']*100:.2f}%",
        "Annualised Return":     f"{metrics['annual_return']*100:.2f}%",
        "Avg Daily Return":      f"{metrics['avg_return']*100:.4f}%",
        "Daily Volatility":      f"{metrics['daily_vol']*100:.4f}%",
        "Annual Volatility":     f"{metrics['annual_vol']*100:.2f}%",
        "Sharpe Ratio":          f"{metrics['sharpe']:.4f}",
        "Maximum Drawdown":      f"{metrics['max_dd']*100:.2f}%",
        "VaR (95%, 1-day)":      f"{metrics['var_95']*100:.4f}%",
        "Positive Days":         f"{metrics['pos_days_pct']*100:.1f}%",
        "Best Single Day":       f"{metrics['best_day']*100:.4f}%",
        "Worst Single Day":      f"{metrics['worst_day']*100:.4f}%",
    }.items()])
    st.dataframe(risk_df, use_container_width=True, hide_index=True)


# ─────────── TAB 3: Indicators ───────────────────────────────────────────────
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_rsi(df, ticker_input), use_container_width=True)
    with col2:
        st.plotly_chart(fig_macd(df, ticker_input), use_container_width=True)

    # BB width chart
    df_bb = df[["Date", "BB_Upper", "BB_Lower", "BB_Mid"]].dropna()
    df_bb["BB_Width"] = ((df_bb["BB_Upper"] - df_bb["BB_Lower"]) / df_bb["BB_Mid"] * 100)
    fig_bbw = go.Figure()
    fig_bbw.add_trace(go.Scatter(
        x=df_bb["Date"], y=df_bb["BB_Width"], name="BB Width",
        fill="tozeroy", fillcolor="rgba(96,165,250,0.08)",
        line=dict(color=COLORS["close"], width=1.5),
    ))
    fig_bbw.update_layout(title=f"{ticker_input} — Bollinger Band Width (Volatility Expansion)",
                          height=280, **PLOT_LAYOUT)
    st.plotly_chart(fig_bbw, use_container_width=True)

    # Latest indicator snapshot
    st.markdown('<p class="section-header">Latest Indicator Snapshot</p>', unsafe_allow_html=True)
    snap = df[["Date", "Close", "SMA_20", "SMA_50", "SMA_200", "EMA_20",
               "RSI_14", "MACD", "MACD_Signal", "BB_Upper", "BB_Lower",
               "Rolling_Vol_20", "Signal"]].tail(10).copy()
    snap["Rolling_Vol_20"] = (snap["Rolling_Vol_20"] * 100).round(2)
    snap["Date"] = snap["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(snap, use_container_width=True, hide_index=True)


# ─────────── TAB 4: Monthly Heatmap ──────────────────────────────────────────
with tab4:
    st.plotly_chart(fig_monthly_heatmap(df, ticker_input), use_container_width=True)

    # Best/worst months
    d = df.copy()
    monthly = (
        d.groupby(["Year", "Month"])["Daily_Return"]
         .apply(lambda r: float((1 + r).prod() - 1) * 100)
         .reset_index()
    )
    monthly.columns = ["Year", "Month", "Return_%"]
    monthly["Month_Name"] = pd.to_datetime(
        monthly["Month"].astype(str), format="%m").dt.strftime("%b")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p class="section-header">🏆 Best 5 Months</p>', unsafe_allow_html=True)
        st.dataframe(
            monthly.nlargest(5, "Return_%")[["Year", "Month_Name", "Return_%"]]
            .rename(columns={"Month_Name": "Month", "Return_%": "Return (%)"})
            .round(2),
            use_container_width=True, hide_index=True
        )
    with col2:
        st.markdown('<p class="section-header">💀 Worst 5 Months</p>', unsafe_allow_html=True)
        st.dataframe(
            monthly.nsmallest(5, "Return_%")[["Year", "Month_Name", "Return_%"]]
            .rename(columns={"Month_Name": "Month", "Return_%": "Return (%)"})
            .round(2),
            use_container_width=True, hide_index=True
        )


# ─────────── TAB 5: Comparison ────────────────────────────────────────────────
with tab5:
    all_tickers = list({ticker_input} | set(compare_tickers))
    dfs = {ticker_input: df}
    with st.spinner("Loading comparison data…"):
        for t in compare_tickers:
            if t != ticker_input:
                dfs[t] = load_data(t, str(start_date), str(end_date))

    valid = {t: d for t, d in dfs.items() if not d.empty}
    if len(valid) > 1:
        st.plotly_chart(fig_comparison(valid), use_container_width=True)

        # Side-by-side risk table
        st.markdown('<p class="section-header">Risk Comparison Table</p>', unsafe_allow_html=True)
        rows = []
        for t, d in valid.items():
            m = compute_risk_metrics(d)
            rows.append({
                "Ticker":          t,
                "Total Return":    f"{m['total_return']*100:.1f}%",
                "Annual Return":   f"{m['annual_return']*100:.1f}%",
                "Annual Vol":      f"{m['annual_vol']*100:.1f}%",
                "Sharpe Ratio":    f"{m['sharpe']:.2f}",
                "Max Drawdown":    f"{m['max_dd']*100:.1f}%",
                "VaR 95%":         f"{m['var_95']*100:.2f}%",
                "Win Rate":        f"{m['pos_days_pct']*100:.1f}%",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("Select at least one ticker in the sidebar to compare.")


# ─────────── TAB 6: Raw Data ─────────────────────────────────────────────────
with tab6:
    st.markdown('<p class="section-header">OHLCV + Indicators Dataset</p>', unsafe_allow_html=True)

    show_cols = ["Date", "Open", "High", "Low", "Close", "Volume",
                 "SMA_20", "SMA_50", "SMA_200", "EMA_20",
                 "Daily_Return", "Cumulative_Return",
                 "RSI_14", "MACD", "MACD_Signal",
                 "BB_Upper", "BB_Mid", "BB_Lower",
                 "Rolling_Vol_20", "Signal",
                 "Golden_Cross", "Death_Cross"]
    display_df = df[show_cols].copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    for col in ["Daily_Return", "Cumulative_Return", "Rolling_Vol_20"]:
        display_df[col] = (display_df[col] * 100).round(4)

    search = st.text_input("🔍 Filter by date (YYYY-MM)", placeholder="e.g. 2023-01")
    if search:
        display_df = display_df[display_df["Date"].str.startswith(search)]

    st.dataframe(display_df.tail(500), use_container_width=True, hide_index=True)

    csv = df[show_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️  Download Full Dataset as CSV",
        data=csv,
        file_name=f"{ticker_input}_analysis_{dt.date.today()}.csv",
        mime="text/csv",
    )


# ─────────── TAB 7: Insights ─────────────────────────────────────────────────
with tab7:
    st.markdown('<p class="section-header">🤖 Automated Analysis Report</p>', unsafe_allow_html=True)

    # Trend
    sma20_latest = df["SMA_20"].dropna().iloc[-1]
    sma50_latest = df["SMA_50"].dropna().iloc[-1]
    sma200_latest = df["SMA_200"].dropna().iloc[-1]
    close_latest  = latest["Close"]

    st.markdown("**📈 Trend Analysis**")
    if close_latest > sma200_latest:
        st.markdown('<div class="insight-positive">✅ Price is above SMA 200 — Long-term uptrend confirmed.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="insight-negative">⚠️ Price is below SMA 200 — Possible long-term downtrend.</div>', unsafe_allow_html=True)

    if sma20_latest > sma50_latest:
        st.markdown('<div class="insight-positive">✅ SMA 20 is above SMA 50 — Short-term bullish momentum.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="insight-negative">⚠️ SMA 20 is below SMA 50 — Short-term bearish pressure.</div>', unsafe_allow_html=True)

    # RSI
    st.markdown("**⚡ Momentum (RSI)**")
    if rsi_now > 70:
        st.markdown(f'<div class="insight-negative">🔴 RSI = {rsi_now:.1f} — Overbought zone. Potential pullback risk.</div>', unsafe_allow_html=True)
    elif rsi_now < 30:
        st.markdown(f'<div class="insight-positive">🟢 RSI = {rsi_now:.1f} — Oversold zone. Potential bounce opportunity.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="insight-neutral">⚪ RSI = {rsi_now:.1f} — Neutral momentum zone.</div>', unsafe_allow_html=True)

    # Volatility
    st.markdown("**📉 Risk & Volatility**")
    ann_vol = metrics['annual_vol'] * 100
    if ann_vol > 40:
        st.markdown(f'<div class="insight-negative">🔴 Annual Volatility = {ann_vol:.1f}% — Highly volatile stock. Higher risk.</div>', unsafe_allow_html=True)
    elif ann_vol > 20:
        st.markdown(f'<div class="insight-neutral">🟡 Annual Volatility = {ann_vol:.1f}% — Moderate volatility.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="insight-positive">🟢 Annual Volatility = {ann_vol:.1f}% — Relatively stable stock.</div>', unsafe_allow_html=True)

    # Sharpe
    st.markdown("**🏆 Risk-Adjusted Performance (Sharpe)**")
    sharpe = metrics["sharpe"]
    if sharpe > 1.5:
        st.markdown(f'<div class="insight-positive">✅ Sharpe Ratio = {sharpe:.2f} — Excellent risk-adjusted returns.</div>', unsafe_allow_html=True)
    elif sharpe > 0.5:
        st.markdown(f'<div class="insight-neutral">⚡ Sharpe Ratio = {sharpe:.2f} — Moderate risk-adjusted returns.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="insight-negative">⚠️ Sharpe Ratio = {sharpe:.2f} — Poor risk-adjusted returns.</div>', unsafe_allow_html=True)

    # Drawdown
    st.markdown("**📊 Drawdown Risk**")
    max_dd = metrics["max_dd"] * 100
    if abs(max_dd) > 40:
        st.markdown(f'<div class="insight-negative">🔴 Max Drawdown = {max_dd:.1f}% — High historical loss from peak.</div>', unsafe_allow_html=True)
    elif abs(max_dd) > 20:
        st.markdown(f'<div class="insight-neutral">🟡 Max Drawdown = {max_dd:.1f}% — Moderate historical peak-to-trough drop.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="insight-positive">🟢 Max Drawdown = {max_dd:.1f}% — Relatively contained downside historically.</div>', unsafe_allow_html=True)

    # MACD
    st.markdown("**🔬 MACD Signal**")
    macd_latest = df["MACD"].dropna().iloc[-1]
    macd_sig_latest = df["MACD_Signal"].dropna().iloc[-1]
    if macd_latest > macd_sig_latest:
        st.markdown(f'<div class="insight-positive">✅ MACD ({macd_latest:.2f}) is above Signal ({macd_sig_latest:.2f}) — Bullish momentum.</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="insight-negative">⚠️ MACD ({macd_latest:.2f}) is below Signal ({macd_sig_latest:.2f}) — Bearish momentum.</div>', unsafe_allow_html=True)

    # Full Summary
    st.divider()
    st.markdown('<p class="section-header">📝 Summary Report</p>', unsafe_allow_html=True)
    report_text = f"""STOCK MARKET ANALYSIS REPORT
Generated: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}
Ticker: {ticker_input} | {company_name}
Period: {str(start_date)} to {str(end_date)}
Sector: {sector} | Industry: {industry}

═══════════════════════════════════════
PERFORMANCE METRICS
═══════════════════════════════════════
Total Return:        {metrics['total_return']*100:.2f}%
Annualised Return:   {metrics['annual_return']*100:.2f}%
Best Single Day:     {metrics['best_day']*100:.4f}%
Worst Single Day:    {metrics['worst_day']*100:.4f}%
Positive Days:       {metrics['pos_days_pct']*100:.1f}%

═══════════════════════════════════════
RISK METRICS
═══════════════════════════════════════
Annual Volatility:   {metrics['annual_vol']*100:.2f}%
Sharpe Ratio:        {metrics['sharpe']:.4f}
Maximum Drawdown:    {metrics['max_dd']*100:.2f}%
VaR (95%, 1-day):    {metrics['var_95']*100:.4f}%

═══════════════════════════════════════
TECHNICAL INDICATORS (LATEST)
═══════════════════════════════════════
Close Price:         ${close_latest:.2f}
SMA 20:              ${sma20_latest:.2f}
SMA 50:              ${sma50_latest:.2f}
SMA 200:             ${sma200_latest:.2f}
RSI (14):            {rsi_now:.2f}
MACD:                {macd_latest:.4f}
MACD Signal:         {macd_sig_latest:.4f}
Current Signal:      {signal_now}
Golden Crosses:      {int(df['Golden_Cross'].sum())}
Death Crosses:       {int(df['Death_Cross'].sum())}

═══════════════════════════════════════
DISCLAIMER
═══════════════════════════════════════
This report is for educational purposes only.
It does not constitute financial advice.
Past performance does not predict future results.
Always consult a licensed financial advisor.
"""
    st.text_area("Full Report", value=report_text, height=420)
    st.download_button(
        "⬇️ Download Report as TXT",
        data=report_text.encode("utf-8"),
        file_name=f"{ticker_input}_report_{dt.date.today()}.txt",
        mime="text/plain",
    )