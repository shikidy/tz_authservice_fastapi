from datetime import datetime

from sqlalchemy import Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


from app.core.settings import config


engine = create_async_engine(config.DB_URL)
session_maker = async_sessionmaker(engine)

class Base(DeclarativeBase):
    ...

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    firstname: Mapped[str] = mapped_column(String(64), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now()) #pylint: disable=e1102
    edited_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now()) #pylint: disable=e1102
