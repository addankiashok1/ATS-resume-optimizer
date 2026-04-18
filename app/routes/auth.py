from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_db
from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    OAuthRequest,
    TokenResponse,
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    payload: SignupRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Email signup.

    Request example:
    {
      "name": "Jane Doe",
      "email": "jane@example.com",
      "password": "StrongP@ssw0rd"
    }

    Response example:
    {
      "access_token": "<jwt>",
      "token_type": "bearer",
      "expires_in": 60
    }
    """
    token = await AuthService.signup(db, payload)
    return token


@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Email login.

    Request example:
    {
      "email": "jane@example.com",
      "password": "StrongP@ssw0rd"
    }
    """
    token = await AuthService.login(db, payload)
    return token


@router.post("/google", response_model=TokenResponse)
async def google_login(
    payload: OAuthRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """Google OAuth login.

    Request example:
    {
      "access_token": "<google-id-token>"
    }
    """
    token = await AuthService.google_login(db, payload)
    return token


@router.post("/linkedin", response_model=TokenResponse)
async def linkedin_login(
    payload: OAuthRequest,
    db: AsyncSession = Depends(get_db),
) -> TokenResponse:
    """LinkedIn OAuth login.

    Request example:
    {
      "access_token": "<linkedin-access-token>"
    }
    """
    token = await AuthService.linkedin_login(db, payload)
    return token
