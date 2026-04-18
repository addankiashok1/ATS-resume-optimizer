from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User, AuthProvider
from app.schemas.auth import SignupRequest, LoginRequest, OAuthRequest, TokenResponse
from app.utils.security import (
    get_password_hash,
    verify_password,
    create_access_token,
)
from app.services.oauth_service import OAuthService


class AuthService:
    @staticmethod
    async def _get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        normalized_email = email.strip().lower()
        result = await db.execute(select(User).where(User.email == normalized_email))
        return result.scalars().first()

    @staticmethod
    async def signup(db: AsyncSession, payload: SignupRequest) -> TokenResponse:
        existing_user = await AuthService._get_user_by_email(db, payload.email)
        if existing_user:
            raise ValueError("A user with that email already exists.")

        password_hash = get_password_hash(payload.password)
        user = User(
            id=uuid.uuid4(),
            name=payload.name.strip(),
            email=payload.email.lower(),
            password_hash=password_hash,
            auth_provider=AuthProvider.email,
            created_at=datetime.utcnow(),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

        return create_access_token(subject=str(user.id), email=user.email)

    @staticmethod
    async def login(db: AsyncSession, payload: LoginRequest) -> TokenResponse:
        user = await AuthService._get_user_by_email(db, payload.email)
        if not user or user.auth_provider != AuthProvider.email:
            raise ValueError("Invalid email or password.")
        if not user.password_hash or not verify_password(payload.password, user.password_hash):
            raise ValueError("Invalid email or password.")

        return create_access_token(subject=str(user.id), email=user.email)

    @staticmethod
    async def google_login(db: AsyncSession, payload: OAuthRequest) -> TokenResponse:
        profile = await OAuthService.verify_google_token(payload.access_token)
        return await AuthService._oauth_login(db, profile, AuthProvider.google)

    @staticmethod
    async def linkedin_login(db: AsyncSession, payload: OAuthRequest) -> TokenResponse:
        profile = await OAuthService.verify_linkedin_token(payload.access_token)
        return await AuthService._oauth_login(db, profile, AuthProvider.linkedin)

    @staticmethod
    async def _oauth_login(db: AsyncSession, profile: dict, provider: AuthProvider) -> TokenResponse:
        if not profile.get("email") or not profile.get("name"):
            raise ValueError("OAuth profile did not include required fields.")

        email = profile["email"].lower()
        user = await AuthService._get_user_by_email(db, email)
        if user:
            if user.auth_provider != provider:
                raise ValueError("Email already registered with a different auth provider.")
            return create_access_token(subject=str(user.id), email=user.email)

        user = User(
            id=uuid.uuid4(),
            name=profile["name"].strip(),
            email=email,
            password_hash=None,
            auth_provider=provider,
            created_at=datetime.utcnow(),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return create_access_token(subject=str(user.id), email=user.email)
