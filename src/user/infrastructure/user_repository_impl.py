from fastapi import Depends
from user.domain.user_repository import UserRepository
from user.domain.user import User
from user.infrastructure.models import UserModel
from shared.core.database import get_db
from sqlalchemy import select

class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session


    def find_by_id(self, user_id: str) -> User | None:
        stmt = select(UserModel).where(UserModel.id == id)
        result = await self.session.execute(stmt)
        user_model = result.scalar_or_none()

        return user_model.to_user()