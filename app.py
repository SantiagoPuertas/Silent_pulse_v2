import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Silent Pulse v2", layout="wide")

@st.cache_data(ttl=3600)
def load_data(tickers, period):
    data = {}

    for t in tickers:
        ticker = yf.Ticker(t)
        df = ticker.history(period=period, auto_adjust=True)

        if df is not None and not df.empty:
            data[t] = df['Close']

    return pd.DataFrame(data)

st.title("Silent Pulse – Market Overview")

# Sidebar
with st.sidebar:
    tickers = st.multiselect(
        "Selecciona acciones",
        ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA"],
        default=["AAPL", "MSFT"]
    )

    period = st.selectbox(
        "Horizonte temporal",
        ["1y", "3y", "5y", "10y"],
        index=2
    )

if not tickers:
    st.warning("Selecciona al menos un ticker")
    st.stop()

df = load_data(tickers, period)

if df.empty:
    st.error("No se pudieron descargar datos.")
    st.stop()

# Normalización tipo demo-stockpeers
df_norm = df / df.iloc[0] * 100

st.line_chart(df_norm)
st.write("Datos actualizados al:", df.index[-1].date())