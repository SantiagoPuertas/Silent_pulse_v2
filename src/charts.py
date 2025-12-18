import pandas as pd
import altair as alt
import streamlit as st

# =========================
# INDICATORS
# =========================

def add_sma(df, window=20):
    df[f"sma_{window}"] = df["close"].rolling(window).mean()
    return df


def add_ema(df, window=20):
    df[f"ema_{window}"] = df["close"].ewm(span=window).mean()
    return df


def add_bollinger(df, window=20):
    sma = df["close"].rolling(window).mean()
    std = df["close"].rolling(window).std()
    df["bb_upper"] = sma + 2 * std
    df["bb_lower"] = sma - 2 * std
    return df


def add_donchian(df, window=20):
    df["donchian_high"] = df["high"].rolling(window).max()
    df["donchian_low"] = df["low"].rolling(window).min()
    return df


def get_support_resistance(df, window=5):
    supports = df[df["low"] == df["low"].rolling(window, center=True).min()]
    resistances = df[df["high"] == df["high"].rolling(window, center=True).max()]
    return supports, resistances


# =========================
# CANDLESTICK CHART
# =========================

def render_candlestick_chart(df, config):
    

    base = alt.Chart(df).encode(
        x=alt.X("date:T", title="Fecha"),
        y=alt.Y("low:Q",title="Precio")
    )

    wicks = base.mark_rule().encode(
        y="low:Q",
        y2="high:Q"
    )

    candles = base.mark_bar().encode(
        y="open:Q",
        y2="close:Q",
        color=alt.condition(
            "datum.open <= datum.close",
            alt.value("#2ecc71"),
            alt.value("#e74c3c")
        )
    )

    layers = [wicks, candles]

    # --- Overlays ---
    if config["sma"]:
        layers.append(
            base.mark_line(color="blue").encode(y="sma_20:Q")
        )

    if config["ema"]:
        layers.append(
            base.mark_line(color="orange").encode(y="ema_20:Q")
        )

    if config["bollinger"]:
        layers.append(
            base.mark_line(color="gray").encode(y="bb_upper:Q")
        )
        layers.append(
            base.mark_line(color="gray").encode(y="bb_lower:Q")
        )

    if config["donchian"]:
        layers.append(
            base.mark_line(color="purple").encode(y="donchian_high:Q")
        )
        layers.append(
            base.mark_line(color="purple").encode(y="donchian_low:Q")
        )

    if config["sr"]:
        supports, resistances = get_support_resistance(df)

        layers.append(
            alt.Chart(supports)
            .mark_point(color="green", size=60)
            .encode(x="date:T", y="low:Q")
        )

        layers.append(
            alt.Chart(resistances)
            .mark_point(color="red", size=60)
            .encode(x="date:T", y="high:Q")
        )

    chart = (
        alt.layer(*layers)
        .properties(height=600)
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

