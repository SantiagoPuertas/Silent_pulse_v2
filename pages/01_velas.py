import streamlit as st
from src.data_loader import load_data, filter_data
from src.charts import render_candlestick_chart

st.set_page_config(
    page_title="Velas por ticker",
    layout="wide"
)

st.title("📊 Gráfico de velas por activo")
st.caption("Visualización OHLC con velas japonesas")

# Load data
df = load_data()

# Sidebar simple para esta página
st.sidebar.title("Configuración")

ticker = st.sidebar.selectbox(
    "Selecciona un ticker",
    sorted(df["ticker"].unique())
)

date_min = df["date"].min()
date_max = df["date"].max()

date_range = st.sidebar.date_input(
    "Rango de fechas",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max
)

# Filter
df_filtered = filter_data(df, [ticker], date_range)

# Chart
render_candlestick_chart(df_filtered, ticker)
