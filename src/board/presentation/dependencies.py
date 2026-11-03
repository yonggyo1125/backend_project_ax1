from board.application.service import BoardService, CommentService, PostService
from board.domain.repository.board_repository import BoardRepository
from board.domain.repository.comment_repository import CommentRepository
from board.domain.repository.post_repository import PostRepository

# Repository 의존성
def provide_board_repository() -> BoardRepository:
    """FastAPI Depends 플레이스홀더 (container.py에서 바인딩)"""
    raise NotImplementedError("BoardRepository 의존성이 주입되지 않았습니다.")


def provide_post_repository() -> PostRepository:
    """FastAPI Depends 플레이스홀더 (container.py에서 바인딩)"""
    raise NotImplementedError("PostRepository 의존성이 주입되지 않았습니다.")


def provide_comment_repository() -> CommentRepository:
    """FastAPI Depends 플레이스홀더 (container.py에서 바인딩)"""
    raise NotImplementedError("CommentRepository 의존성이 주입되지 않았습니다.")


# Service 의존성
def provide_board_service() -> BoardService:
    """FastAPI Depends 플레이스홀더 (container.py에서 바인딩)"""
    raise NotImplementedError("BoardService 의존성이 주입되지 않았습니다.")


def provide_post_service() -> PostService:
    """FastAPI Depends 플레이스홀더 (container.py에서 바인딩)"""
    raise NotImplementedError("PostService 의존성이 주입되지 않았습니다.")


def provide_comment_service() -> CommentService:
    """FastAPI Depends 플레이스홀더 (container.py에서 바인딩)"""
    raise NotImplementedError("CommentService 의존성이 주입되지 않았습니다.")