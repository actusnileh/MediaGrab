from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from common.settings import settings

if settings.mode == "TEST":
    DATABASE_URL = f"postgresql+asyncpg://{settings.test_db_username}:{settings.test_db_password}@{settings.test_db_host}:{settings.test_db_port}/{settings.test_db_name}"
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = f"postgresql+asyncpg://{settings.db_username}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
