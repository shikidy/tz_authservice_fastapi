import json
from datetime import datetime, timedelta, timezone
from typing import Literal, TypedDict

import jwt
from passlib.context import CryptContext #type: ignore

from app.core.settings import config


class EncodedJWT(TypedDict):
    token: str
    expired_at: datetime

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWTType = Literal["access", "secret"]

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def hash_password(plain_password) -> str:
    return password_context.hash(plain_password)

def decode_jwt_token(encoded: str, type_: JWTType) -> dict:
    key = config.ACCESS_KEY if type_ == "access" else config.SECRET_KEY
    algo = config.ACCESS_ALGO if type_ == "access" else config.SECRET_ALGO
    decoded = jwt.decode(encoded, key=key, algorithms=[algo])
    return json.loads(decoded["sub"])

def encode_jwt_token(data: dict, type_: JWTType) -> EncodedJWT:
    key = config.ACCESS_KEY if type_ == "access" else config.SECRET_KEY
    algo = config.ACCESS_ALGO if type_ == "access" else config.SECRET_ALGO
    alive_minutes = timedelta(
        minutes=config.ACCESS_ALIVE_MIN if type_ == "access" else config.SECRET_ALIVE_MIN
    )
    expired_at = datetime.now(timezone.utc) + alive_minutes
    to_encode = {
        "exp": expired_at,
        "sub": json.dumps(data, default=str, indent=4, sort_keys=True)
    }
    
    return {
        "expired_at": expired_at,
        "token": jwt.encode(
            payload=to_encode,
            key=key,
            algorithm=algo
        )
    }
