from fastapi import FastAPI
from user.presentation.routers.v1.router import router as user_router

app = FastAPI(
    title="쇼핑몰 API", 
    description="설명...",
    version="1.0.0"
)


app.include_router(user_router)
