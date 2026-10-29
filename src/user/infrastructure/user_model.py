import uuid
from datetime import datetime, timezone
from shared.core.models import Base
from sqlalchemy import String, Boolean, DateTime, Uuid
from sqlalchemy.orm import Mapped, mapped_column

class UserModel(Base):
    __tablename__ = "USERS"
    
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )

    email: Mapped[str] = mapped_column(
        String(85),
        unique=True,
        index=True,
        nullable=False,
        comment="로그인 이메일"
    )

    password: Mapped[str] = mapped_column(
        String(65),
        comment="로그인 비밀번호"
    )

    name: Mapped[str] = mapped_column(
        String(45),
        index=True,
        nullable=False,
        comment="회원명"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="생성 일시(UTC)"
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="수정 일시(UTC)"
    )

    deleted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        comment="삭제 일시(UTC)"
    )


