import streamlit as st

def render_sidebar(df):
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

    return selected_tickers, date_range
