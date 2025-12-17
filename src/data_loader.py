import pandas as pd
import streamlit as st
from pathlib import Path

DATA_PATH = Path("data/sp500_prices.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    return df.sort_values("date")


def filter_data(df, tickers, date_range):
    return df[
        (df["ticker"].isin(tickers)) &
        (df["date"] >= pd.to_datetime(date_range[0])) &
        (df["date"] <= pd.to_datetime(date_range[1]))
    ]
