from typing import Optional
from abc import ABC, abstractmethod
from user.domain.user import User

class UserRepository(ABC):

    @abstractmethod
    def find_by_id(self, user_id: str) -> User | None:
        ...
