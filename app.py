import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Silent Pulse v2", layout="wide")

API_KEY = st.secrets["ALPHAVANTAGE_API_KEY"]

@st.cache_data(ttl=3600)
def load_data(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",  # 👈 FREE
        "symbol": symbol,
        "apikey": API_KEY,
        "outputsize": "compact"
    }

    r = requests.get(url, params=params)
    data = r.json()

    # ⛔ Rate limit o error
    if "Note" in data or "Error Message" in data:
        return None

    ts = data.get("Time Series (Daily)")
    if ts is None:
        return None

    df = pd.DataFrame.from_dict(ts, orient="index", dtype=float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Usamos cierre normal (free)
    df = df[["4. close"]].rename(columns={"4. close": symbol})

    return df

st.title("Silent Pulse – Market Overview")

with st.sidebar:
    ticker = st.selectbox(
        "Activo",
        ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA"]
    )

df = load_data(ticker)

if df is None or df.empty:
    st.error("No se pudieron obtener datos (límite de API o endpoint incorrecto).")
    st.stop()

df_norm = df / df.iloc[0] * 100
st.line_chart(df_norm)
