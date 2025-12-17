import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Silent Pulse v2", layout="wide")

API_KEY = "75XHQD8DX1SP3OV6"

@st.cache_data(ttl=3600)
def load_data(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "compact"
    }
    r = requests.get(url, params=params)
    data = r.json()

    ts = data.get("Time Series (Daily)")
    if ts is None:
        return None

    df = pd.DataFrame.from_dict(ts, orient="index", dtype=float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    return df[["5. adjusted close"]].rename(columns={"5. adjusted close": symbol})

st.title("Silent Pulse – Market Overview")

with st.sidebar:
    ticker = st.selectbox(
        "Activo",
        ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA"]
    )

df = load_data(ticker)

if df is None or df.empty:
    st.error("No se pudieron obtener datos.")
    st.stop()

df_norm = df / df.iloc[0] * 100
st.line_chart(df_norm)
