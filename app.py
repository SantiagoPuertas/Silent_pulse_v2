import streamlit as st
from src.data_loader import load_data, filter_data
from src.sidebar import render_sidebar
from src.metrics import render_metrics
from src.tables import render_data_table


# -------------------------
# CONFIG
# -------------------------
st.set_page_config(
    page_title="Stock Dashboard",
    layout="wide",
)

# -------------------------
# LOAD DATA
# -------------------------
df = load_data()

# -------------------------
# SIDEBAR
# -------------------------
selected_tickers, date_range = render_sidebar(df)

# -------------------------
# FILTER DATA
# -------------------------
df_filtered = filter_data(df, selected_tickers, date_range)

# -------------------------
# HEADER
# -------------------------
st.title("📈 Stock Prices Dashboard")
st.caption("Datos históricos de cotizaciones – visualización en Streamlit")

# -------------------------
# METRICS
# -------------------------
render_metrics(df_filtered, selected_tickers)


# -------------------------
# TABLE
# -------------------------
render_data_table(df_filtered)
