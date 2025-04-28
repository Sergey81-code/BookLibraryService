from typing import Any
from uuid import UUID


from db.base_repository import BaseRepository


class BaseService():
    def __init__(self, repo: BaseRepository):
        self.repo = repo


    async def _get_only_existing_objects(self, objects: list[Any | UUID], key: str = "id") -> list[Any] | list:
        if not objects:
            return []
        received_obj_ids = [
            getattr(obj, key) if hasattr(obj, key)
            else obj[key] if isinstance(obj, dict) and key in obj
            else obj
            for obj in objects
        ]
        return await self.repo.get_all(
            [lambda model: model.id.in_(received_obj_ids)],
        )
    