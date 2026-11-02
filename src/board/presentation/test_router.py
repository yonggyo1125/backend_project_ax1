from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from board.infrastructure.models import Board, Post
from shared.core.database import get_db

router = APIRouter(prefix="/test")

@router.get("/1")
async def test1(session: AsyncSession = Depends(get_db)):
    board = Board(
        id="qna",
        name="제목1"
    )

    session.add(board)
    await session.commit()
    await session.refresh(board)
