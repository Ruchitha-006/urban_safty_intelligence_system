from fastapi import APIRouter

from backend.schemas import (
    RouteRequest,
)

from backend.services.safe_route import (
    get_safe_route,
)


router = APIRouter(
    prefix="/api/route",
    tags=["Safe Route"],
)


@router.post("/safe")
def safe_route(
    payload: RouteRequest,
):

    return get_safe_route(
        origin_lat=payload.origin_lat,
        origin_lon=payload.origin_lon,
        destination_lat=payload.destination_lat,
        destination_lon=payload.destination_lon,
    )