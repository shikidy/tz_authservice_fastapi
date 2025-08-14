from fastapi import FastAPI

from app.api import api_router
from app.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)
