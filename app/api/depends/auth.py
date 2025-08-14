from typing import Annotated

import jwt
import pydantic
from fastapi import Depends, Header, HTTPException, status

from app.core.security import decode_jwt_token
from app.models.user import AccessTokenData
from app.repository.models import UserModel
from .repository import UserRepositoryDep


async def get_user(user: UserRepositoryDep, auth: Annotated[str, Header(alias="authorization")]) -> UserModel:
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    splited_header = auth.split(" ")

    if len(splited_header) != 2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    access_token = splited_header[1]

    try:
        decoded_access = decode_jwt_token(access_token, "access")
    except (jwt.DecodeError, jwt.ExpiredSignatureError) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e
    
    try:
        parsed_access = AccessTokenData.model_validate(decoded_access)
    except pydantic.ValidationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e
    
    fetched_user = await user.get(id=parsed_access.user_id)

    if fetched_user is None or fetched_user.edited_at > parsed_access.created_at:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    return fetched_user

GetUserDep = Annotated[UserModel, Depends(get_user)]
