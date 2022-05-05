from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app import settings

db_connection_str = settings.db_async_connection_str


async_engine = create_async_engine(
    db_connection_str,
    echo=True,
    future=True
)


async def get_async_session() -> AsyncSession:
    async_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


sync_engine = create_engine(
    settings.db_sync_connection_str,
    echo=True,
    future=True
)


def get_sync_session() -> Session:
    sync_session = sessionmaker(sync_engine, expire_on_commit=False)
    return sync_session()