from datetime import datetime, timedelta

import jwt

from app.config import settings

EXPIRATION_TIME = timedelta(hours=4)


def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, settings.SECRET_AUTH, algorithm=settings.ALGORITHM)
    return token


def verify_jwt_token(token: str):
    try:
        decoded_data = jwt.decode(
            token, settings.SECRET_AUTH, algorithms=[settings.ALGORITHM]
        )
        return decoded_data
    except jwt.PyJWTError:
        return None
