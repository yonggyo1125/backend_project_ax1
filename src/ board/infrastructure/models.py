from datetime import datetime,timezone
from sqlalchemy import String, Text, Integer, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from shared.core.models import Base


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    name: Mapped[str] = mapped_column(String(65), nullable=False)
    write_role[str] = mapped_column(String(30), default="ALL", nullable=False)
    is_active[boolean] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=datetime.now(timezone.utc),
        nullable=False
    )

    modified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        nullable=True, 
        onupdate=datetime.now(timezone.utc)
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )