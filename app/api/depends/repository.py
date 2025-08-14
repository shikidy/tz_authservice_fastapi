from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.models import session_maker
from app.repository.user_repository import UserRepository


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as ses:
        yield ses

DBDep = Annotated[AsyncSession, Depends(get_db)]

async def user_repository(session: DBDep) -> UserRepository:
    return UserRepository(session)

UserRepositoryDep = Annotated[UserRepository, Depends(user_repository)]
