from functools import partial
from uuid import UUID

from fastapi import APIRouter, Depends

from api.core.dependencies.role_required import role_required
from api.core.dependencies.services import get_author_service
from api.v1.authors.schemas import AuthorCreate, AuthorUpdate, ShowAuthor
from api.v1.authors.service import AuthorService
from utils.roles import PortalRole

author_router = APIRouter()

@author_router.get('/{author_id}', response_model=ShowAuthor)
async def get_author(
        author_id: UUID,
        author_service: AuthorService = Depends(get_author_service),
    ) -> ShowAuthor:
    return await author_service.get_author_by_id(author_id)


@author_router.post(
        '/', 
        response_model=ShowAuthor, 
        dependencies=[role_required([PortalRole.ROLE_PORTAL_ADMIN, PortalRole.ROLE_PORTAL_SUPERADMIN])]
    )
async def create_author(
        body: AuthorCreate,
        author_service: AuthorService = Depends(get_author_service),
    ) -> ShowAuthor:
    author = await author_service.create_author_orm_obj(body)
    return await author_service.create_author_in_database(author)


@author_router.patch(
        '/', 
        response_model=ShowAuthor, 
        dependencies=[role_required([PortalRole.ROLE_PORTAL_ADMIN, PortalRole.ROLE_PORTAL_SUPERADMIN])]
    )
async def update_authors(
        author_id: UUID,
        body: AuthorUpdate,
        author_service: AuthorService = Depends(get_author_service),
    ) -> ShowAuthor:
    author = await author_service.get_author_by_id(author_id)
    return await author_service.update_author(author, body)


@author_router.delete(
        "/",
        dependencies=[role_required([PortalRole.ROLE_PORTAL_ADMIN, PortalRole.ROLE_PORTAL_SUPERADMIN])]
    )
async def delete_author(
    author_id: UUID,
    author_service: AuthorService = Depends(get_author_service),
) -> UUID:
    return await author_service.delete_author_by_id(author_id)



@author_router.get("/", response_model=ShowAuthor)
async def get_authors_by_name(
    author_name: str,
    author_service: AuthorService = Depends(get_author_service),
) -> ShowAuthor:
    return await author_service.get_author_by_name(author_name)