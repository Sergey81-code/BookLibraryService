from typing import Any, Callable, Generic, Type, TypeVar
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy.ext.asyncio import AsyncSession


T = TypeVar("T")
ObjID = UUID | str | int

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
    
    async def add(self, session: AsyncSession, obj_in: T) -> T:
        session.add(obj_in)
        await session.commit()
        await session.refresh(obj_in)
        return obj_in
    
    async def get_by_id(self, session: AsyncSession, obj_id: ObjID) -> T | None:
        result = await session.execute(select(self.model).where(self.model.id == obj_id))
        return result.scalars().first()
    
    async def delete_objects_by_ids(self, session: AsyncSession, obj_ids: list[ObjID]) -> list[ObjID] | None:
        stmt = (
            delete(self.model)
            .where(self.model.id.in_(obj_ids))
            .returning(self.model.id)
        )
        result = await session.execute(stmt)
        await session.commit()
        deleted_ids = result.scalars().all()
        return deleted_ids if deleted_ids else None
    
    async def get_all(
            self,
            session: AsyncSession,
            object_filters: list[Callable[[Type[DeclarativeBase]], BinaryExpression]] | None = None
        ):
        stmt = select(self.model)
        if object_filters:
            for object_filter in object_filters:
                stmt = stmt.where(object_filter(self.model))
        results = await session.execute(stmt)
        return results.scalars().all()
    
    async def update_obj(self, session: AsyncSession, obj: T, updated_params: dict[str, Any]) -> T:
        query = (
            update(self.model)
            .where(self.model.id == obj.id)
            .values(updated_params)
            .returning(self.model)
        )
        
            
        res = await session.execute(query)
        await session.commit()
        updated_obj = res.scalars().first()
        await session.refresh(updated_obj)
        return updated_obj

