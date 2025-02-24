import asyncio
from models import Base as MyBase
from session import async_engine

async def create_tables(Base):
    async with async_engine.begin() as conn:
        # Создаем таблицы
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await create_tables(MyBase)


if __name__ == "__main__":
    asyncio.run(main())