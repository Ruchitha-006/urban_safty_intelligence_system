from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data" / "crimes.csv"


def _fallback_data() -> pd.DataFrame:
    rows = [
        ["2026-01-01", "Bengaluru", "Theft", 12.9716, 77.5946, 2],
        ["2026-01-03", "Bengaluru", "Robbery", 12.9750, 77.6000, 4],
        ["2026-01-05", "Bengaluru", "Assault", 12.9680, 77.5900, 4],
        ["2026-01-08", "Bengaluru", "Theft", 12.9720, 77.5970, 2],
        ["2026-01-11", "Bengaluru", "Fraud", 12.9800, 77.6100, 2],
        ["2026-01-13", "Bengaluru", "Robbery", 12.9700, 77.6030, 4],
        ["2026-01-17", "Bengaluru", "Assault", 12.9755, 77.5960, 5],
        ["2026-01-20", "Bengaluru", "Theft", 12.9690, 77.5890, 2],
        ["2026-01-23", "Bengaluru", "Burglary", 12.9780, 77.6050, 3],
        ["2026-01-25", "Bengaluru", "Robbery", 12.9810, 77.6000, 5],
        ["2026-01-28", "Bengaluru", "Fraud", 12.9670, 77.5950, 2],
        ["2026-02-01", "Bengaluru", "Theft", 12.9730, 77.5920, 2],
    ]

    return pd.DataFrame(
        rows,
        columns=[
            "date",
            "city",
            "crime_type",
            "latitude",
            "longitude",
            "severity",
        ],
    )


def load_crime_data() -> pd.DataFrame:
    if DATA_PATH.exists():
        dataframe = pd.read_csv(DATA_PATH)
    else:
        dataframe = _fallback_data()

    dataframe["date"] = pd.to_datetime(
        dataframe["date"],
        errors="coerce",
    )

    dataframe["latitude"] = pd.to_numeric(
        dataframe["latitude"],
        errors="coerce",
    )

    dataframe["longitude"] = pd.to_numeric(
        dataframe["longitude"],
        errors="coerce",
    )

    dataframe["severity"] = pd.to_numeric(
        dataframe["severity"],
        errors="coerce",
    ).fillna(1)

    dataframe = dataframe.dropna(
        subset=[
            "latitude",
            "longitude",
        ]
    )

    return dataframe


def predict_hotspots() -> list[dict]:
    dataframe = load_crime_data()

    coordinates = dataframe[
        [
            "latitude",
            "longitude",
        ]
    ].to_numpy()

    if len(coordinates) < 3:
        return []

    # Approximate degree-to-distance scaling.
    scaled = coordinates * np.array(
        [
            111.0,
            111.0,
        ]
    )

    clustering = DBSCAN(
        eps=0.8,
        min_samples=2,
    )

    labels = clustering.fit_predict(scaled)

    dataframe["cluster"] = labels

    hotspots = []

    for cluster_id in sorted(
        set(labels)
    ):

        if cluster_id == -1:
            continue

        cluster = dataframe[
            dataframe["cluster"] == cluster_id
        ]

        center_lat = float(
            cluster["latitude"].mean()
        )

        center_lon = float(
            cluster["longitude"].mean()
        )

        crime_count = int(
            len(cluster)
        )

        risk_score = float(
            min(
                100,
                (
                    cluster["severity"].mean()
                    * 15
                    + crime_count * 8
                ),
            )
        )

        hotspots.append(
            {
                "cluster": int(cluster_id),
                "latitude": center_lat,
                "longitude": center_lon,
                "crime_count": crime_count,
                "risk_score": round(
                    risk_score,
                    2,
                ),
            }
        )

    return hotspots


def crime_stats() -> dict:
    dataframe = load_crime_data()

    total = int(
        len(dataframe)
    )

    high_severity = int(
        (
            dataframe["severity"] >= 4
        ).sum()
    )

    average_severity = float(
        dataframe["severity"].mean()
    )

    crime_types = (
        dataframe["crime_type"]
        .value_counts()
        .head(8)
        .to_dict()
    )

    return {
        "total_crimes": total,
        "high_severity": high_severity,
        "average_severity": round(
            average_severity,
            2,
        ),
        "crime_types": crime_types,
    }