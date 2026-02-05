from datetime import datetime, timedelta, timezone
from jose import jwt
from app_tools.jwt_config import jwt_settings


def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        jwt_settings.SECRET_KEY,
        algorithm=jwt_settings.JWT_ALGORITHM,
    )
