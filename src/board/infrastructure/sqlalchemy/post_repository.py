from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from board.domain.post import Post
from board.domain.repository.post_repository import PostRepository
from board.domain.enums import PostSearchType
from board.infrastructure.sqlalchemy.mappers import PostMapper
from board.infrastructure.sqlalchemy.models import PostModel
from user.infrastructure.models import UserModel

class SqlAlchemyPostRepository(PostRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    def _build_search_filter(
        self,
        search_type: PostSearchType | str | None,
        keyword: str | None
    ):
        """검색 조건에 따른 필터 표현식 생성"""
        if not keyword or not keyword.strip():
            return None

        clean_keyword = keyword.strip()

        if isinstance(search_type, str):
            try:
                search_type = PostSearchType(search_type.upper())
            except ValueError:
                search_type = PostSearchType.ALL
        elif search_type is None:
            search_type = PostSearchType.ALL

        author_email_expr = UserModel.email.icontains(clean_keyword)
        author_name_expr = PostModel.author_name.icontains(clean_keyword)
        title_expr = PostModel.title.icontains(clean_keyword)
        content_expr = PostModel.content.ilike(clearn_keyword)

        match search_type:
            case PostSearchType.TITLE:
                return title_expr
            case PostSearchType.CONTENT:
                return content_expr
            case PostSearchType.TITLE_CONTENT:
                return or_(title_expr, content_expr)
            case PostSearchType.AUTHOR_EMAIL:
                return author_email_expr
            case PostSearchType.AUTHOR_NAME:
                return author_name_expr
            case PostSearchType.ALL:
                return or_(
                    title_expr,
                    content_expr,
                    author_name_expr,
                    author_email_expr,
                )        


    async def find_by_id(self, post_id: int) -> Post | None:
        """게시글 ID 기준으로 단건 조회 (삭제된 글 제외)"""
        stmt = select(PostModel).where(
            PostModel.post_id == post_id,
            PostModel.deleted_at.is_(None),
        )

        model = await self.session.scalar(stmt)
        return PostMapper.to_domain(model) if model else None

    async def find_by_board_id(
        self,
        board_id: str,
        limit: int,
        offset: int,
        search_type: PostSearchType | str | None = None,
        keyword: str | None = None,
    ) -> list[Post]:
        """특정 게시판의 게시글 목록을 최신순으로 페이징 조회"""
        stmt = (
            select(PostModel)
            .where(
                PostModel.board_id == board_id,
                PostModel.deleted_at.is_(None)
            )
        )

        # 키워드 검색 조건 추가
        search_condition = self._build_search_filter(search_type, keyword)
        if search_condition is not None:
            stmt = stmt.where(search_condition)

        # 페이징 및 정렬
        stmt = stmt.order_by(PostModel.post_id.desc()).offset(offset).limit(limit)

        models = (await self.session.scalars(stmt)).all()
        return [PostMapper.to_domain(model) for model in models]

    async def count_by_board_id(
        self, 
        board_id: str,
        search_type: PostSearchType | str | None = None,
        keyword: str | None = None,
    ) -> int:
        """특정 게시판의 전체 유효 게시글 수 카운트 (페이지네이션 계산용)"""
        stmt = (
            select(func.count(PostModel.post_id))
            .where(
                PostModel.board_id == board_id,
                PostModel.deleted_at.is_(None),
            )
        )

        search_condition = self._build_search_filter(search_type, keyword)
        if search_condition is not None:
            stmt = stmt.where(search_condition)

        count = await self.session.scalar(stmt)
        return count or 0

    @abstractmethod
    async def save(self, post: Post) -> Post:
        """게시글 등록 또는 수정"""
        if post.post_id:
            _post = await self._session.get(PostModel, post.post_id)
            if _post:
                _post.title = post.title
                _post.content = post.content
                _post.deleted_at = post.deleted_at
                await self.session.commit()
                await self.session.refresh(_post)
                return PostMapper.to_domain(_post)

        new_model = PostMapper.to_model(post)
        self.session.add(new_model)
        await self.session.commit()
        await self.session.refresh(new_model)
        return PostMapper.to_domain(new_model)