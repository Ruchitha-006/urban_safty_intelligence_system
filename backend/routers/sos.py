from fastapi import (
    APIRouter,
    Request,
)

from backend.schemas import (
    SOSRequest,
)

from backend.services.sos import (
    trigger_sos,
)


router = APIRouter(
    prefix="/api/sos",
    tags=["SOS"],
)


@router.post("/")
def create_sos(
    request: Request,
    payload: SOSRequest,
):

    username = request.session.get(
        "username"
    )

    return trigger_sos(
        username=username,
        latitude=payload.latitude,
        longitude=payload.longitude,
        message=payload.message,
    )