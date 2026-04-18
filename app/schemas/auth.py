from datetime import datetime
from enum import Enum
from typing import Optional
import re
from pydantic import BaseModel, EmailStr, Field, field_validator


def validate_password_strength(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    rules = [
        r"[a-z]",
        r"[A-Z]",
        r"\d",
        r"[^A-Za-z0-9]",
    ]
    matches = sum(bool(re.search(rule, value)) for rule in rules)
    if matches < 3:
        raise ValueError(
            "Password must include at least three of the following: lowercase, uppercase, number, special character."
        )
    return value


class AuthProvider(str, Enum):
    email = "email"
    google = "google"
    linkedin = "linkedin"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class SignupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        return validate_password_strength(value)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        return validate_password_strength(value)


class OAuthRequest(BaseModel):
    access_token: str = Field(..., min_length=10)


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    auth_provider: AuthProvider
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
