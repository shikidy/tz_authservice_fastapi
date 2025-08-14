import jwt
from fastapi import APIRouter, status, HTTPException
import pydantic

from app.api.depends import UserRepositoryDep, GetUserDep
from app.models.user import (
    UserCreate, RefreshTokenCreate, 
    TokenCreated, RefreshTokenData,
    AccessTokenCreate, AccessTokenData,
    UserData
)
from app.core.security import hash_password, verify_password, encode_jwt_token, decode_jwt_token


user_router = APIRouter(prefix="/user")

@user_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, user: UserRepositoryDep):
    fetched_user = await user.get(email=data.email)

    if fetched_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already used"
        )
    
    await user.create(
        email=data.email,
        firstname=data.firstname,
        password_hash=hash_password(data.password)
    )

@user_router.post("/refresh_token", status_code=status.HTTP_200_OK)
async def create_refresh(data: RefreshTokenCreate, user: UserRepositoryDep) -> TokenCreated:
    fetched_user = await user.get(email=data.email)

    if fetched_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not verify_password(data.password, fetched_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    token_data = RefreshTokenData(
        user_id=fetched_user.id,
        created_at=fetched_user.edited_at
    )

    encoded_token = encode_jwt_token(
        data=token_data.model_dump(),
        type_="secret"
    )
    
    return TokenCreated(
        token=encoded_token["token"],
        type="refresh",
        expires_at=encoded_token["expired_at"]
    )

@user_router.post("/access_token")
async def create_access(data: AccessTokenCreate, user: UserRepositoryDep) -> TokenCreated:
    try:
        decoded_refresh = decode_jwt_token(data.refresh_token, type_="secret")
    except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e

    try:
        parsed_refresh = RefreshTokenData.model_validate(
            decoded_refresh
        )
    except pydantic.ValidationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e
    
    fetched_user = await user.get(id=parsed_refresh.user_id)

    if fetched_user is None or fetched_user.edited_at > parsed_refresh.created_at:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    access_data = AccessTokenData(
        user_id=fetched_user.id,
        created_at=fetched_user.edited_at
    )

    encoded_jwt = encode_jwt_token(access_data.model_dump(), type_="access")

    return TokenCreated(
        token=encoded_jwt["token"],
        type="access",
        expires_at=encoded_jwt["expired_at"]
    )

@user_router.get("/")
async def me(user: GetUserDep) -> UserData:
    return UserData(
        email=user.email,
        firstname=user.firstname
    )
