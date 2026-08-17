from backend.database import create_sos_event


def trigger_sos(
    username: str | None,
    latitude: float,
    longitude: float,
    message: str,
) -> dict:

    create_sos_event(
        username=username,
        latitude=latitude,
        longitude=longitude,
        message=message,
    )

    return {
        "success": True,
        "message": (
            "SOS event recorded successfully."
        ),
        "latitude": latitude,
        "longitude": longitude,
    }