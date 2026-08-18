from fastapi import APIRouter, HTTPException

from backend.services.hotspot import (
    crime_stats,
    predict_hotspots,
)

from backend.services.forecasting import (
    forecast,
)

from backend.services.fir_classifier import (
    classify_fir,
)

from backend.schemas import (
    FIRRequest,
)


router = APIRouter(
    prefix="/api/crime",
    tags=["Crime Intelligence"],
)


@router.get("/stats")
def stats():
    return crime_stats()


@router.get("/hotspots")
def hotspots():
    return {
        "hotspots": predict_hotspots()
    }


@router.get("/forecast")
def crime_forecast():
    return {
        "forecast": forecast(
            days=30
        )
    }


@router.post("/fir")
def fir_classification(
    payload: FIRRequest,
):

    try:

        return classify_fir(
            payload.text
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )