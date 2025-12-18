import streamlit as st
import plotly.graph_objects as go


def render_candlestick_chart(df):
    """
    Gráfico de velas interactivo con Plotly.
    Sin indicadores.
    """

    df = df.sort_values("date")

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["date"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                increasing_line_color="#26a69a",
                decreasing_line_color="#ef5350",
                name="Precio"
            )
        ]
    )

    fig.update_layout(
        height=650,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Fecha",
        yaxis_title="Precio",
        xaxis_rangeslider_visible=False,
        template="plotly_white"
    )

    fig.update_xaxes(
        showgrid=True,
        rangeslider_visible=False
    )

    fig.update_yaxes(
        showgrid=True,
        fixedrange=False  # permite zoom vertical
    )

    st.plotly_chart(fig, use_container_width=True)
