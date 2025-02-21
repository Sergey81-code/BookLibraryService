from db.session import async_session
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db():
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
