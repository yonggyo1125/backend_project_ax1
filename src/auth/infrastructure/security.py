
import os
import uuid
import jwt
from datetime import datetime, timezone, timedelta

from auth.domain.entities import TokenPayload
from auth.domain.service import TokenProvider

class JwtTokenProvider(TokenProvider):
    def __init__(
        self,
        secret_key: str = os.getenv("JWT_SECRET_KEY"),
        algorithm: str = "HS512",
        access_token_expire_minutes: int = 60
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = access_token_expire_minutes

    # access token 생성
    def create_access_token(self, user_id: UUID) -> tuple[str, str, datetime, int]:
        """(token, jti, expired_at, expires_in_seconds) 반환"""
        now = datetime.now(timezone.utc)
        expires_delta = timedelta(minutes=self.expire_minutes)
        expired_at = now + expires_delta
        expires_in = int(expires_delta.total_seconds())
        jti = str(uuid.uuid4())

        payload = {
            "sub": str(user_id),
            "jti": jti,
            "exp": expired_at,
            "iat": now
        }

        encoded_jwt = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        return encoded_jwt, jti, expired_at, expires_in


    def decode_token(self, token: str) -> TokenPayload:
        """토큰 검증 및 페이로드 추출"""
        pass