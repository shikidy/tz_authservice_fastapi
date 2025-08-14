from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator


PasswordField = Field(
    max_length=32,
    min_length=8
)
class UserCreate(BaseModel):
    email: EmailStr
    firstname: str = Field(
        max_length=12, 
        min_length=3,
        examples=["Alex", "Johna"],
        pattern=r"^[a-zA-Z]+$"
    )
    password: str = PasswordField

    @field_validator("firstname")
    @classmethod
    def validate_name(cls, v: str):
        if not v.isalpha():
            raise ValueError("Name must contain only letters")
        return v.capitalize()
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least 1 uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least 1 lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least 1 digit")
        if not any(c in "!@#$%^&*()_+-=[]{};':\",.<>/?\\" for c in v):
            raise ValueError("Password must contain at least 1 special character")
        return v

class RefreshTokenCreate(BaseModel):
    email: EmailStr
    password: str = PasswordField

class TokenCreated(BaseModel):
    token: str
    type: Literal["refresh", "access"]
    expires_at: datetime

class RefreshTokenData(BaseModel):
    user_id: int
    created_at: datetime

class AccessTokenCreate(BaseModel):
    refresh_token: str = Field(
        min_length=20
    )

class AccessTokenData(BaseModel):
    user_id: int
    created_at: datetime

class UserData(BaseModel):
    email: str
    firstname: str