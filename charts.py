import plotly.graph_objects as go
import streamlit as st

def render_candlestick_chart(df, ticker):
    df_t = df[df["ticker"] == ticker].sort_values("date")

    if df_t.empty:
        st.warning("No hay datos para el ticker seleccionado")
        return

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df_t["date"],
                open=df_t["open"],
                high=df_t["high"],
                low=df_t["low"],
                close=df_t["close"],
                name=ticker
            )
        ]
    )

    fig.update_layout(
        title=f"Gráfico de velas – {ticker}",
        xaxis_title="Fecha",
        yaxis_title="Precio ($)",
        xaxis_rangeslider_visible=False,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
