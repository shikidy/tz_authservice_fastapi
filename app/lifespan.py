from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.settings import config
from app.repository.user_repository import UserRepository
from app.repository.models import session_maker
from app.core.security import hash_password


async def create_test_user():
    async with session_maker() as ses:
        user_repository = UserRepository(ses)
        fetched_user = await user_repository.get(email=config.TEST_EMAIL)
        if fetched_user is None:
            await user_repository.create(
                email=config.TEST_EMAIL,
                firstname="Somename",
                password_hash=hash_password(config.TEST_PASSWORD)
            )

@asynccontextmanager
async def lifespan(app: FastAPI): #pylint: disable=w0613
    if config.is_local is True:
        await create_test_user()
    yield
