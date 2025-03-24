import datetime
from jose import jwt

from api.core.config import get_settings


settings = get_settings()

async def create_jwt_token(roles: list[str]) -> str:
        token_key = settings.SECRET_KEY_FOR_ACCESS
        token_time = 30
        to_encode = {"roles" : roles}
        expire = datetime.datetime.now(datetime.timezone.utc) + \
            datetime.timedelta(minutes=token_time)
        to_encode.update({"sub": "test@mail.ru"})
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, token_key, algorithm=settings.ALGORITHM)


async def create_auth_headers_for_user(roles: list[str]) -> dict[str]:
    token = await create_jwt_token(roles)
    return {"Authorization": f"Bearer {token}"}