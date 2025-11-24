from datetime import date

import pandas as pd
from plotly import graph_objects as go
import streamlit as st

CANDLE_COLUMNS = {"open", "close", "high", "low"}
REQUIRED_COLUMNS = {"date": date, "ticker": str}


def validate_data(df: pd.DataFrame) -> bool:
    if df.empty:
        st.write("The data file is empty. Please upload a file with data in it.")
        return False

    if missing_columns := set(REQUIRED_COLUMNS) - set(df.columns):
        missing_column_report = "\n- ".join(
            [f"{column} ({REQUIRED_COLUMNS[column]})" for column in missing_columns]
        )

        st.write(
            f"The data is missing the required columns:\n- {missing_column_report}"
        )
        return False

    wrong_column_types = {
        column: (required_type, type(df[column].iat[0]))
        for column, required_type in REQUIRED_COLUMNS.items()
        if not isinstance(df[column].iat[0], required_type)
    }
    if wrong_column_types:
        column_type_output = "\n- ".join(
            [
                f'Column "{column}" is {actual_type} (should be {required_type})'
                for column, (required_type, actual_type) in wrong_column_types.items()
            ]
        )
        st.write(f"The data has the wrong column data types:\n\n- {column_type_output}")
        return False

    return True


def main():
    st.write("Analyze your data!")

    with st.container(border=True):
        uploaded_file = st.file_uploader("Upload a data file", type=["parquet"])

    if not uploaded_file:
        st.write("Please upload a file.")
        return

    data = pd.read_parquet(uploaded_file)

    if not validate_data(data):
        return

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
    for index, chart in enumerate(charts, start=1):
        if isinstance(chart, go.Figure):
            tabs[index].plotly_chart(chart)
        else:
            tabs[index].line_chart(chart)


if __name__ == "__main__":
    main()
