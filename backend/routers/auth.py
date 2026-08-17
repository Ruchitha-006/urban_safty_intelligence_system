import hashlib
import hmac
import secrets

from fastapi import (
    APIRouter,
    Request,
)

from backend.database import (
    create_user,
    get_user,
)

from backend.schemas import (
    APIResponse,
    LoginRequest,
    RegisterRequest,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


def hash_password(
    password: str,
) -> str:

    salt = secrets.token_hex(
        16
    )

    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        120000,
    )

    return (
        f"{salt}:{derived.hex()}"
    )


def verify_password(
    password: str,
    stored: str,
) -> bool:

    try:

        salt, stored_hash = (
            stored.split(":")
        )

        derived = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            120000,
        )

        return hmac.compare_digest(
            derived.hex(),
            stored_hash,
        )

    except ValueError:
        return False


@router.post(
    "/register",
    response_model=APIResponse,
)
def register(
    payload: RegisterRequest,
):

    password_hash = hash_password(
        payload.password
    )

    created = create_user(
        username=payload.username,
        email=payload.email,
        password_hash=password_hash,
        city=payload.city,
    )

    if not created:

        return APIResponse(
            success=False,
            message=(
                "Username or email already exists."
            ),
        )

    return APIResponse(
        success=True,
        message=(
            "Registration successful."
        ),
    )


@router.post(
    "/login",
    response_model=APIResponse,
)
def login(
    request: Request,
    payload: LoginRequest,
):

    user = get_user(
        payload.username
    )

    if user is None:

        return APIResponse(
            success=False,
            message=(
                "Invalid username or password."
            ),
        )

    if not verify_password(
        payload.password,
        user["password_hash"],
    ):

        return APIResponse(
            success=False,
            message=(
                "Invalid username or password."
            ),
        )

    request.session["username"] = (
        user["username"]
    )

    request.session["city"] = (
        user["city"]
    )

    return APIResponse(
        success=True,
        message="Login successful.",
    )


@router.post(
    "/logout",
    response_model=APIResponse,
)
def logout(
    request: Request,
):

    request.session.clear()

    return APIResponse(
        success=True,
        message="Logged out.",
    )


@router.get("/me")
def me(
    request: Request,
):

    return {
        "authenticated": (
            "username" in request.session
        ),
        "username": request.session.get(
            "username"
        ),
        "city": request.session.get(
            "city"
        ),
    }