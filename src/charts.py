import altair as alt
import streamlit as st

def render_price_chart(df_filtered):
    st.subheader("Evolución del precio")

    chart = (
        alt.Chart(df_filtered)
        .mark_line(interpolate="monotone")
        .encode(
            x=alt.X("date:T", title="Fecha"),
            y=alt.Y("close:Q", title="Precio de cierre ($)"),
            color=alt.Color("ticker:N", title="Ticker"),
            tooltip=["ticker", "date", "close"]
        )
        .properties(height=450)
    )

    st.altair_chart(chart, use_container_width=True)
