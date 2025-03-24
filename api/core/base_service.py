from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from db.base_repository import BaseRepository

T = TypeVar("T")

class BaseService(Generic[T]):
    def __init__(self, repo: BaseRepository[T]):
        self.repo = repo


    async def _get_only_existing_objects(self, objects: list[T | UUID], session: AsyncSession, key: str = "id") -> list[T] | list:
        if not objects:
            return []
        received_obj_ids = [
            getattr(obj, key) 
            if isinstance(obj, self.repo.model) 
            else obj
            for obj in objects 
            ]
        return await self.repo.get_all(
            session,
            [lambda model: model.id.in_(received_obj_ids)],
        )
    