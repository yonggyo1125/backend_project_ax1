from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from shared.core.models import Base, DateTimeBase

class BoardModel(Base, DateTimeBase):
    """게시판 설정 테이블"""
    __tablename__ = "boards"

    board_id: Mapped[str] = mapped_column(String(30), primary_key=True)
    board_name: Mapped[str] = mapped_column(String(100), nullable=False)
    page_size: Mapped[int] = mapped_column(Integer, default=20, nullable=False)

    # 게시판 권한
    edit_role: Mapped[str] = mapped_column(String(20), default="ALL", nullable=False)
    view_role: Mapped[str] = mapped_column(String(20), default="ALL", nullable=False)
    list_role: Mapped[str] = mapped_column(String(20), default="ALL", nullable=False)
    comment_list_role: Mapped[str] = mapped_column(String(20), default="ALL", nullable=False)
    comment_edit_role: Mapped[str] = mapped_column(String(20), default="ALL", nullable=False)

class PostModel(DateTimeBase):
    pass