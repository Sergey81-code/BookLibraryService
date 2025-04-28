from fastapi import Depends, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from api.core.exceptions import AppExceptions

from utils.jwt import JWT

from api.core.config import get_settings

settings = get_settings()


async def get_user_token(credentials: HTTPAuthorizationCredentials = Security(security := HTTPBearer())):
    token = credentials.credentials
    return await JWT.decode_jwt_token(token, "access")


def role_required(required_roles: list[str] = Query(None, include_in_schema=False)):
    
    if settings.ENABLE_ROLE_CHECK == False:

        async def skip_check_role():
            return
        return Depends(skip_check_role)
    
    async def role_check(
        user_decode_token = Depends(get_user_token)
    ):
        roles: list[str] | None = user_decode_token.get("roles", [])
        required_user_roles = [role for role in roles if role in required_roles]
        if not required_user_roles:
            AppExceptions.forbidden_exception("Forbidden: insufficient permissions")
        return
    return Depends(role_check)
    