from fastapi import Depends, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from api.core.exceptions import AppExceptions
from api.v1.authors.repository import AuthorRepository
from api.v1.authors.service import AuthorService
from api.v1.books.repository import BookRepository
from api.v1.books.service import BookService
from db.session import async_session

from utils.jwt import JWT


async def get_session():
    """Dependency for getting async session"""
    async with async_session() as session:
        yield session

async def get_book_service(repo: BookRepository = Depends()):
    return BookService(repo)

async def get_author_service(repo: AuthorRepository = Depends()):
    return AuthorService(repo)


async def get_user_token(credentials: HTTPAuthorizationCredentials = Security(security := HTTPBearer())):
    token = credentials.credentials
    return await JWT.decode_jwt_token(token, "access")


async def role_required(required_roles: list[str] = Query(None, include_in_schema=False), user_decode_token = Depends(get_user_token)):
    roles: list[str] | None = user_decode_token.get("roles", [])
    required_user_roles = [role for role in roles if role in required_roles]
    if not required_user_roles:
        AppExceptions.forbidden_exception("Forbidden: insufficient permissions")
    yield
    