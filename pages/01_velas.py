import streamlit as st
from src.data_loader import load_data
from src.charts import (
    add_sma,
    add_ema,
    add_bollinger,
    add_donchian,
    render_candlestick_chart
)


# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="Velas",
    layout="wide"
)

st.title("📊 Gráfico de velas")

# -------------------------
# LOAD DATA
# -------------------------
df = load_data()

ticker = st.selectbox(
    "Selecciona ticker",
    sorted(df["ticker"].unique())
)

df = df[df["ticker"] == ticker].copy()

# -------------------------
# SIDEBAR - TECHNICALS
# -------------------------
st.sidebar.subheader("📐 Análisis técnico")

show_sma = st.sidebar.checkbox("SMA 20")
show_ema = st.sidebar.checkbox("EMA 20")
show_bb = st.sidebar.checkbox("Bandas de Bollinger")
show_donchian = st.sidebar.checkbox("Canal Donchian")
show_sr = st.sidebar.checkbox("Soportes / Resistencias")

# -------------------------
# ADD INDICATORS
# -------------------------
df = add_sma(df, 20)
df = add_ema(df, 20)
df = add_bollinger(df, 20)
df = add_donchian(df, 20)

config = {
    "sma": show_sma,
    "ema": show_ema,
    "bollinger": show_bb,
    "donchian": show_donchian,
    "sr": show_sr
}

# -------------------------
# CHART
# -------------------------
render_candlestick_chart(df, config)
