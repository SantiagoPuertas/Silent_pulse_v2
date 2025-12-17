import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="Stock Dashboard",
    layout="wide",
)

DATA_PATH = Path("data/sp500_prices.csv")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    return df.sort_values("date")

df = load_data()

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.title("📊 Stock selector")

tickers = sorted(df["ticker"].unique())
selected_tickers = st.sidebar.multiselect(
    "Selecciona empresas",
    tickers,
    default=tickers[:3]
)

date_min = df["date"].min()
date_max = df["date"].max()

date_range = st.sidebar.date_input(
    "Rango de fechas",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)

# -------------------------
# FILTER DATA
# -------------------------
df_filtered = df[
    (df["ticker"].isin(selected_tickers)) &
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1]))
]

# -------------------------
# HEADER
# -------------------------
st.title("📈 Stock Prices Dashboard")
st.caption("Datos históricos de cotizaciones – visualización en Streamlit")

# -------------------------
# METRICS
# -------------------------
if not df_filtered.empty:
    cols = st.columns(len(selected_tickers))

    for col, ticker in zip(cols, selected_tickers):
        df_t = df_filtered[df_filtered["ticker"] == ticker]

        first = df_t.iloc[0]["close"]
        last = df_t.iloc[-1]["close"]
        variation = (last / first - 1) * 100

        col.metric(
            label=ticker,
            value=f"{last:,.2f} $",
            delta=f"{variation:.2f} %"
        )

# -------------------------
# LINE CHART
# -------------------------
st.subheader("Evolución del precio")

line_chart = (
    alt.Chart(df_filtered)
    .mark_line(interpolate="monotone")
    .encode(
        x=alt.X("date:T", title="Fecha"),
        y=alt.Y("close:Q", title="Precio de cierre ($)"),
        color=alt.Color("ticker:N", title="Ticker"),
        tooltip=["ticker", "date", "close"]
    )
    .properties(height=450)
)

st.altair_chart(line_chart, use_container_width=True)

# -------------------------
# DATA TABLE
# -------------------------
with st.expander("📄 Ver datos en tabla"):
    st.dataframe(
        df_filtered.sort_values(["ticker", "date"], ascending=[True, False]),
        use_container_width=True
    )
