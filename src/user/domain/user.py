import uuid
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: uuid.UUID
    email: str
    name: str
    resign: bool  # 탈퇴 여부
    created_at: datetime
    modified_at: datetime | None
    deleted_at: datetime | None

    def __post__init__(self):
         
        pass    