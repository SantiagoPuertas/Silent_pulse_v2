import streamlit as st

def render_metrics(df_filtered, selected_tickers):
    if df_filtered.empty:
        return

    cols = st.columns(len(selected_tickers))

    for col, ticker in zip(cols, selected_tickers):
        df_t = df_filtered[df_filtered["ticker"] == ticker]

        first = df_t.iloc[0]["close"]
        last = df_t.iloc[-1]["close"]
        variation = (last / first - 1) * 100

        col.metric(
            label=ticker,
            value=f"{last:,.2f} $",
            delta=f"{variation:.2f} %"
        )
