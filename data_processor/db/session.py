from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

engine = create_async_engine(
    "postgresql+asyncpg://"
    +"postgresql+asyncpg://postgres:postgres@db:5432/devdb".split("?")[0].split("://")[1],
    future=True,
    echo=False,
    pool_pre_ping=True,
    poolclass=NullPool,
)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)
