from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class NoteCreate(BaseModel):
    title: str
    content: str

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip()

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip()


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty")
        return v.strip() if v else v

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Content cannot be empty")
        return v.strip() if v else v


class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    is_pinned: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ShareRequest(BaseModel):
    share_with_email: EmailStr


class NoteSearchResponse(NoteResponse):
    owner_email: Optional[str] = None
