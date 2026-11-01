from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from shared.core.database import get_db
from user.application.service import UserService
from user.infrastructure.repositories import SqlAlchemyUserRepository
from user.infrastructure.security import BcryptPasswordHasher
from user.presentation.routers.v1.router import provide_user_service

_password_hasher = BcryptPasswordHasher()

def create_user_service(
    session: AsyncSession = Depends(get_db)
) -> UserService:
    repository = SqlAlchemyUserRepository(session)
    return UserService(
        repository=repository, 
        hasher=_password_hasher
    )   


def wire_dependencies(app: FastAPI) -> None:
    app.dependency_overrides.update(
        {
            provide_user_service: create_user_service
        }
    )
