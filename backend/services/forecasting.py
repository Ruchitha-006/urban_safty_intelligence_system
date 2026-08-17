from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "crimes.csv"


def _load():
    from .hotspot import load_crime_data

    dataframe = load_crime_data()

    if dataframe.empty:
        return dataframe

    monthly = (
        dataframe
        .set_index("date")
        .resample("ME")
        .size()
        .rename("count")
        .reset_index()
    )

    return monthly


def forecast(days: int = 30) -> list[dict]:
    monthly = _load()

    if monthly.empty:
        return []

    counts = monthly["count"].to_numpy(
        dtype=float
    )

    if len(counts) == 1:
        trend = np.repeat(
            counts[0],
            days,
        )

    else:
        x = np.arange(
            len(counts)
        )

        coefficients = np.polyfit(
            x,
            counts,
            1,
        )

        future_x = np.arange(
            len(counts),
            len(counts) + days,
        )

        trend = np.polyval(
            coefficients,
            future_x,
        )

        trend = np.maximum(
            trend,
            0,
        )

    last_date = pd.Timestamp.now().normalize()

    results = []

    for i, value in enumerate(trend):

        date = (
            last_date
            + pd.Timedelta(
                days=i + 1
            )
        )

        results.append(
            {
                "date": date.strftime(
                    "%Y-%m-%d"
                ),
                "predicted_cases": round(
                    float(value),
                    2,
                ),
            }
        )

    return results