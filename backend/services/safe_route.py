import math
from typing import Optional

import requests


OSRM_URL = (
    "https://router.project-osrm.org/route/v1/driving/"
)


def _distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:

    radius = 6371.0

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    delta_phi = math.radians(
        lat2 - lat1
    )

    delta_lambda = math.radians(
        lon2 - lon1
    )

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1)
        * math.cos(phi2)
        * math.sin(delta_lambda / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a),
    )

    return radius * c


def _fallback_route(
    origin_lat: float,
    origin_lon: float,
    destination_lat: float,
    destination_lon: float,
) -> dict:

    distance = _distance_km(
        origin_lat,
        origin_lon,
        destination_lat,
        destination_lon,
    )

    duration = (
        distance / 30
    ) * 60

    return {
        "success": True,
        "distance_km": round(
            distance,
            2,
        ),
        "duration_min": round(
            duration,
            2,
        ),
        "route": [
            {
                "latitude": origin_lat,
                "longitude": origin_lon,
            },
            {
                "latitude": destination_lat,
                "longitude": destination_lon,
            },
        ],
        "source": "fallback-straight-line",
    }


def get_safe_route(
    origin_lat: float,
    origin_lon: float,
    destination_lat: float,
    destination_lon: float,
) -> dict:

    try:

        coordinates = (
            f"{origin_lon},{origin_lat};"
            f"{destination_lon},{destination_lat}"
        )

        response = requests.get(
            OSRM_URL + coordinates,
            params={
                "overview": "full",
                "geometries": "geojson",
            },
            timeout=8,
        )

        response.raise_for_status()

        payload = response.json()

        if not payload.get(
            "routes"
        ):
            return _fallback_route(
                origin_lat,
                origin_lon,
                destination_lat,
                destination_lon,
            )

        route = payload["routes"][0]

        geometry = route[
            "geometry"
        ]["coordinates"]

        points = [
            {
                "latitude": point[1],
                "longitude": point[0],
            }
            for point in geometry
        ]

        return {
            "success": True,
            "distance_km": round(
                route["distance"] / 1000,
                2,
            ),
            "duration_min": round(
                route["duration"] / 60,
                2,
            ),
            "route": points,
            "source": "OSRM",
        }

    except (
        requests.RequestException,
        KeyError,
        ValueError,
    ):

        return _fallback_route(
            origin_lat,
            origin_lon,
            destination_lat,
            destination_lon,
        )