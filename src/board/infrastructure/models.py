from datetime import datetime,timezone
from sqlalchemy import String, Text, BigInteger, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from shared.core.models import Base


class Board(Base):
    """게시판 설정"""
    __tablename__ = "boards"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(65), nullable=False)
    write_role: Mapped[str] = mapped_column(String(30), default="ALL", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

    modified_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True), nullable=True, onupdate=datetime.now(timezone.utc))

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

class Post(Base):
    __tablename__ = "posts"
    
    id: Mapped[int] = mapped_column(
        BigInteger, 
        primary_key=True, 
        autoincrement=True
    )

    category: Mapped[str] = mapped_column(
        String(60),
        nullable=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False)

    modified_at: Mapped[datetime | None] = mapped_column(
    DateTime(timezone=True), nullable=True, onupdate=datetime.now(timezone.utc))

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # 외래키 
    board_id: Mapped[str] = mapped_column(
        ForeignKey("boards.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # 게시판 설정(N:1)
    board_config: Mapped["Board"] = relationship()
