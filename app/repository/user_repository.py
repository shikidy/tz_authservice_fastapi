from typing import Optional

from sqlalchemy import select

from .base_repository import BaseRepository
from .models import UserModel


class UserRepository(BaseRepository):


    async def create(
        self,
        *,
        email: str,
        firstname: str,
        password_hash: str
    ) -> UserModel:
        new_user = UserModel(
            email=email,
            firstname=firstname,
            password_hash=password_hash
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def get(
        self,
        *,
        id: Optional[int] = None,
        email: Optional[str] = None
    ) -> Optional[UserModel]:
        stmt = select(UserModel)

        if id is not None:
            stmt = stmt.where(UserModel.id == id)
        elif email is not None:
            stmt = stmt.where(UserModel.email == email)
        else:
            raise ValueError("Id or Email should be provided")
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
        