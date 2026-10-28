from typing import Annotated
from fastapi import APIRouter, Path

router = APIRouter(prefix="/v1/user", tags=["User"])

# 회원가입
@router.post("")
async def sign_up():
    pass

# 회원정보 조회
@router.get("/{user_id}")
async def get_user(
    user_id: Annotated[str, Path(description="회원 아이디")]
):
    pass



