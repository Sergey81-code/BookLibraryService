import sys
import os

from sqlalchemy import create_engine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


sync_engine = create_engine(settings.SYNC_REAL_DATABASE_URL, future=True, echo=True)
async_engine = create_async_engine(settings.ASYNC_REAL_DATABASE_URL, future=True, echo=True)

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

async def get_session():
    async with async_session() as session:
        yield session
