import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.config.database import Base


class AuthProvider(str, PyEnum):
    email = "email"
    google = "google"
    linkedin = "linkedin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(length=255), nullable=False)
    email = Column(String(length=255), nullable=False, unique=True, index=True)
    password_hash = Column(String(length=255), nullable=True)
    auth_provider = Column(Enum(AuthProvider, name="auth_provider"), nullable=False, default=AuthProvider.email)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
