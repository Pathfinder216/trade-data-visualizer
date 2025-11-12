import pandas as pd
from plotly import graph_objects as go
import streamlit as st

st.write("Analyze your data!")

with st.container(border=True):
    uploaded_file = st.file_uploader("Upload a data file", type=["parquet"])

if uploaded_file:
    data = pd.read_parquet(uploaded_file)

    with st.container(border=True):
        ticker = st.selectbox("Ticker", data["ticker"].unique())
        data = data.where(data["ticker"] == ticker)

    candlestick = go.Candlestick(
        x=data["date"],
        open=data["open"],
        close=data["close"],
        high=data["high"],
        low=data["low"],
    )
    layout = go.Layout(title=ticker, xaxis={"title": "Date"}, yaxis={"title": "Price"})
    figure = go.Figure(data=[candlestick], layout=layout)

    tab1, tab2 = st.tabs(["Chart", "Dataframe"])
    tab1.plotly_chart(figure)
    tab2.dataframe(data, height=250, width="stretch")
else:
    st.write("Please upload a file")
