from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

# Auth 도메인
from auth.application.service import AuthService
from auth.domain.repository import TokenBlacklistRepository
from auth.domain.service import TokenProvider, UserCredentialVerifier
from auth.infrastructure.credentials_verifier import UserCredentialVerifierImpl
from auth.infrastructure.repositories import SqlAlchemyTokenBlacklistRepository
from auth.infrastructure.security import JwtTokenProvider
from auth.presentation.dependencies import provide_auth_service

# Board 도메인
from board.application.service import BoardService, CommentService, PostService
from board.domain.repository.board_repository import BoardRepository
from board.domain.repository.comment_repository import CommentRepository
from board.domain.repository.post_repository import PostRepository
from board.domain.service import PasswordHasher as BoardPasswordHasherInterface
from board.infrastructure.security import BcryptPasswordHasher as BoardBcryptPasswordHasher
from board.infrastructure.sqlalchemy.board_repository import SqlAlchemyBoardRepository
from board.infrastructure.sqlalchemy.comment_repository import SqlAlchemyCommentRepository
from board.infrastructure.sqlalchemy.post_repository import SqlAlchemyPostRepository
from board.presentation.dependencies import (
    provide_board_repository,
    provide_board_service,
    provide_comment_repository,
    provide_comment_service,
    provide_post_repository,
    provide_post_service,
)

# Shared
from shared.core.database import get_db

# User 도메인
from user.application.service import UserService
from user.domain.repository import UserRepository
from user.domain.service import PasswordHasher as UserPasswordHasherInterface
from user.infrastructure.repositories import SqlAlchemyUserRepository
from user.infrastructure.security import BcryptPasswordHasher as UserBcryptPasswordHasher
from user.presentation.dependencies import (
    provide_user_repository,
    provide_user_service,
)

# 싱글턴 유틸리티 인스턴스 
_user_password_hasher: UserPasswordHasherInterface = UserBcryptPasswordHasher()
_board_password_hasher: BoardPasswordHasherInterface = BoardBcryptPasswordHasher()
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
        hasher=_user_password_hasher,
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
        password_hasher=_user_password_hasher,
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

# Board 도메인
def create_board_repository(
    session: AsyncSession = Depends(get_db),
) -> BoardRepository:
    return SqlAlchemyBoardRepository(session)


def create_post_repository(
    session: AsyncSession = Depends(get_db),
) -> PostRepository:
    return SqlAlchemyPostRepository(session)


def create_comment_repository(
    session: AsyncSession = Depends(get_db),
) -> CommentRepository:
    return SqlAlchemyCommentRepository(session)


def create_board_service(
    board_repo: BoardRepository = Depends(create_board_repository),
) -> BoardService:
    return BoardService(board_repo=board_repo)


def create_post_service(
    post_repo: PostRepository = Depends(create_post_repository),
    board_repo: BoardRepository = Depends(create_board_repository),
) -> PostService:
    return PostService(
        post_repo=post_repo,
        board_repo=board_repo,
        password_hasher=_board_password_hasher,
    )


def create_comment_service(
    comment_repo: CommentRepository = Depends(create_comment_repository),
    post_repo: PostRepository = Depends(create_post_repository),
    board_repo: BoardRepository = Depends(create_board_repository),
) -> CommentService:
    return CommentService(
        comment_repo=comment_repo,
        post_repo=post_repo,
        board_repo=board_repo,
        password_hasher=_board_password_hasher,
    )

# FastAPI Dependency Overrides 와이어링
def wire_dependencies(app: FastAPI) -> None:
    app.dependency_overrides.update(
        {
            # User
            provide_user_repository: create_user_repository,
            provide_user_service: create_user_service,
            
            # Auth
            provide_auth_service: create_auth_service,
            
            # Board
            provide_board_repository: create_board_repository,
            provide_post_repository: create_post_repository,
            provide_comment_repository: create_comment_repository,
            provide_board_service: create_board_service,
            provide_post_service: create_post_service,
            provide_comment_service: create_comment_service,
        }
    )