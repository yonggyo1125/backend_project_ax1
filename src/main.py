from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from shared.core.models import Base
from shared.core.database import engine, close_db
from user.presentation.routers.v1.router import router as user_router
from shared.core.schemas import APIResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 모델 임포트
    import user.infrastructure.models

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # 애플리케이션 종료시 커넥션 풀 정리
    await close_db()

app = FastAPI(
    title="쇼핑몰 API", 
    description="설명...",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(user_router)