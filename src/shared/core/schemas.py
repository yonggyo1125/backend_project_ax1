from typing import TypeVar, Optional, Generic, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime, timezone

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    success: bool = Field(description="처리 성공/실패 여부")
    message: Optional[str] = Field(None, description="성공 또는 실패시 설명")
    errors: Optional[Dict[str, List[str]]] = Field(None, description="실패시 필드별 오류 메세지")
    data: Optional[T] = Field(None, description="성공시 응답 데이터")
    responded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="응답 날짜시간(UTC)")

