import altair as alt
import streamlit as st


def render_candlestick_chart(df):
    """
    Gráfico de velas OHLC simple, limpio e interactivo.
    Sin indicadores.
    """

    # Aseguramos orden temporal
    df = df.sort_values("date")

    base = alt.Chart(df).encode(
        x=alt.X(
            "date:T",
            title="Fecha",
            axis=alt.Axis(format="%Y-%m-%d", labelAngle=-45)
        )
    )

    # Mechas (high-low)
    wicks = base.mark_rule().encode(
        y=alt.Y("low:Q", title="Precio"),
        y2="high:Q"
    )

    # Cuerpo de las velas
    candles = base.mark_bar(size=6).encode(
        y="open:Q",
        y2="close:Q",
        color=alt.condition(
            "datum.close >= datum.open",
            alt.value("#26a69a"),  # verde
            alt.value("#ef5350")   # rojo
        )
    )

    chart = (
        alt.layer(wicks, candles)
        .properties(
            height=600
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)
