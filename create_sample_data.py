import random
from typing import Any

import pandas as pd
from datetime import datetime


def create_entry(ticker: str, day: int) -> dict[str, Any]:
    open_value = random.randint(0, 100)
    close_value = random.randint(0, 100)
    high_value = random.randint(max(open_value, close_value), 100)
    low_value = random.randint(0, min(open_value, close_value))

    average = random.randint(low_value, high_value)
    other_data = random.random()

    return {
        "ticker": ticker,
        "date": datetime(2025, 1, day).date(),
        "open": open_value,
        "close": close_value,
        "low": low_value,
        "high": high_value,
        "average": average,
        "other_data": other_data,
    }


if __name__ == "__main__":
    tickers = ("MSFT", "NVDA", "TSLA")

    data = [create_entry(ticker, day) for ticker in tickers for day in range(1, 11)]

    df = pd.DataFrame(data)
    df.to_parquet("sample_data.parquet")
