from typing import Callable
from uuid import UUID
import asyncpg


class TestDAL:
    def __init__(self, asyncpg_pool: asyncpg.Pool):
        self.pool = asyncpg_pool

    async def get_obj_from_database_by_id(self, tablename: str, obj_id: UUID) -> asyncpg.Record | None:
        query = f"""
            SELECT * FROM {tablename}
            WHERE id = $1 
        """
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, obj_id)
        
    async def get_all(
            self, 
            tablename: str, 
            object_filters: list[Callable[[str], str]] | None = None
            ) -> list[asyncpg.Record] | list:
        query = f"""SELECT * FROM {tablename}"""

        if object_filters:
            filters = [filter_func(tablename) for filter_func in object_filters]
            query += " WHERE " + " AND ".join(filters)

        async with self.pool.acquire() as connection:
            result = await connection.fetch(query)
            return [record for record in result]
        
        
    
    async def create_object_in_database(self, tablename: str, obj: dict, field_to_return: str = "id") -> str | None:
        columns = "\"" + "\", \"".join(obj.keys()) + "\""
        value_placeholders = ", ".join([f"${i+1}" for i in range(len(obj))])
        values = tuple(obj.values())
        query = f"""
            INSERT INTO {tablename} ({columns})
            VALUES ({value_placeholders})
            RETURNING {field_to_return}
        """
        async with self.pool.acquire() as connection:
            return await connection.fetchval(query, *values)