from fastapi import APIRouter

from .user import user_router


v1_api_router = APIRouter(prefix="/v1")
v1_api_router.include_router(user_router)
