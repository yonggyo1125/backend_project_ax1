from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.service import AuthService
from auth.domain.service import TokenProvider, UserCredentialVerifier
from auth.domain.repository import TokenBlacklistRepository
from auth.infrastructure.repositories import SqlAlchemyTokenBlacklistRepository
from auth.infrastructure.security import JwtTokenProvider
from auth.infrastructure.credentials_verifier import UserCredentialVerifierImpl
from auth.presentation.dependencies import provide_auth_service
from shared.core.database import get_db
from user.application.service import UserService
from user.domain.repository import UserRepository
from user.infrastructure.repositories import SqlAlchemyUserRepository
from user.infrastructure.security import BcryptPasswordHasher
from user.presentation.dependencies import (
    provide_user_repository,
    provide_user_service,
)

# 싱글턴 유틸리티 인스턴스 
_password_hasher = BcryptPasswordHasher()
_token_provider: TokenProvider = JwtTokenProvider()

# User 도메인
def create_user_repository(
    session: AsyncSession = Depends(get_db),
) -> UserRepository:
    return SqlAlchemyUserRepository(session)


def create_user_service(
    repository: UserRepository = Depends(create_user_repository),
) -> UserService:
    return UserService(
        repository=repository,
        hasher=_password_hasher,
    )


# Auth 도메인
def create_token_blacklist_repository(
    session: AsyncSession = Depends(get_db),
) -> TokenBlacklistRepository:
    return SqlAlchemyTokenBlacklistRepository(session)

def create_credential_verifier(
    user_repository: UserRepository = Depends(create_user_repository),
) -> UserCredentialVerifier:
    return UserCredentialVerifierImpl(
        user_repo=user_repository,
        password_hasher=_password_hasher,
    )

def create_auth_service(
    credential_verifier: UserCredentialVerifier = Depends(create_credential_verifier),
    blacklist_repository: TokenBlacklistRepository = Depends(create_token_blacklist_repository),
) -> AuthService:
    return AuthService(
        credential_verifier=credential_verifier,
        token_blacklist_repo=blacklist_repository,
        token_provider=_token_provider,
    )

# FastAPI Dependency Overrides 와이어링
def wire_dependencies(app: FastAPI) -> None:
    app.dependency_overrides.update(
        {
            provide_user_repository: create_user_repository,
            provide_user_service: create_user_service,
            provide_auth_service: create_auth_service,
        }
    )