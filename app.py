import pandas as pd
from plotly import graph_objects as go
import streamlit as st

CANDLE_COLUMNS = ("open", "close", "high", "low")

st.write("Analyze your data!")

with st.container(border=True):
    uploaded_file = st.file_uploader("Upload a data file", type=["parquet"])

if uploaded_file:
    data = pd.read_parquet(uploaded_file)

    with st.container(border=True):
        ticker = st.selectbox("Ticker", data["ticker"].unique())
        data = data.where(data["ticker"] == ticker)

    tab_names = ["Dataframe"]
    charts = []
    if all(column in data.columns for column in CANDLE_COLUMNS):
        candles_chart = go.Candlestick(
            x=data["date"],
            open=data["open"],
            close=data["close"],
            high=data["high"],
            low=data["low"],
        )
        candles_layout = go.Layout(
            title=ticker, xaxis={"title": "Date"}, yaxis={"title": "Price"}
        )
        candles_figure = go.Figure(data=[candles_chart], layout=candles_layout)

        tab_names.append("Candles")
        charts.append(candles_figure)

    for column in data.columns:
        if column in ("ticker", "date") or column in CANDLE_COLUMNS:
            continue

        tab_names.append(column)
        charts.append(data[[column, "date"]].set_index("date"))

    tabs = st.tabs(tab_names)
    tabs[0].dataframe(data, height=250, width="stretch")
    for index, (tab_name, chart) in enumerate(zip(tab_names[1:], charts), start=1):
        if isinstance(chart, go.Figure):
            tabs[index].plotly_chart(chart)
        else:
            tabs[index].line_chart(chart)
else:
    st.write("Please upload a file")
