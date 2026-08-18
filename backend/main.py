from pathlib import Path

from fastapi import (
    FastAPI,
)
from fastapi.middleware.cors import (
    CORSMiddleware,
)
from fastapi.responses import (
    FileResponse,
)
from fastapi.staticfiles import (
    StaticFiles,
)
from starlette.middleware.sessions import (
    SessionMiddleware,
)

from backend.database import init_db

from backend.routers.auth import (
    router as auth_router,
)

from backend.routers.crime import (
    router as crime_router,
)

from backend.routers.route import (
    router as route_router,
)

from backend.routers.sos import (
    router as sos_router,
)


BASE_DIR = Path(
    __file__
).resolve().parent.parent

FRONTEND_DIR = (
    BASE_DIR / "frontend"
)

STATIC_DIR = (
    FRONTEND_DIR / "static"
)


app = FastAPI(
    title="Urban Safety Intelligence System",
    description=(
        "AI-powered urban safety platform"
    ),
    version="1.0.0",
)


app.add_middleware(
    SessionMiddleware,
    secret_key=(
        "urban-safety-intelligence-secret-2026"
    ),
    max_age=60 * 60 * 24 * 7,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if STATIC_DIR.exists():

    app.mount(
        "/static",
        StaticFiles(
            directory=str(
                STATIC_DIR
            )
        ),
        name="static",
    )


app.include_router(
    auth_router
)

app.include_router(
    crime_router
)

app.include_router(
    route_router
)

app.include_router(
    sos_router
)


@app.on_event("startup")
def startup():

    init_db()


@app.get("/")
def home():

    return FileResponse(
        str(
            FRONTEND_DIR
            / "index.html"
        )
    )


@app.get("/login")
def login_page():

    return FileResponse(
        str(
            FRONTEND_DIR
            / "login.html"
        )
    )


@app.get("/dashboard")
def dashboard_page():

    return FileResponse(
        str(
            FRONTEND_DIR
            / "dashboard.html"
        )
    )


@app.get("/health")
def health():

    return {
        "status": "ok",
        "application": (
            "Urban Safety Intelligence System"
        ),
    }