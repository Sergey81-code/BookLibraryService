from jose import JWTError, jwt
from api.core.config import get_settings
from api.core.exceptions import AppExceptions


settings = get_settings()

class JWT:
    @staticmethod
    async def decode_jwt_token(token: str, token_type: str) -> dict[str, str]:
        if token_type == "access":
            token_key = settings.SECRET_KEY_FOR_ACCESS
        try:
            payload = jwt.decode(token, token_key, algorithms=[settings.ALGORITHM])
            if "sub" not in payload.keys():
                AppExceptions.unauthorized_exception("Could not validate credentials")
        except JWTError:
            AppExceptions.unauthorized_exception("Could not validate credentials")
        return payload
