from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker,
)

from app.core.config import configs


if configs.mode == "TEST":
    DATABASE_URL = (
        f"postgresql+asyncpg://{configs.test_db_username}:{configs.test_db_password}@"
        f"{configs.test_db_host}:{configs.test_db_port}/{configs.test_db_name}"
    )
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = (
        f"postgresql+asyncpg://{configs.db_username}:{configs.db_password}@"
        f"{configs.db_host}:{configs.db_port}/{configs.db_name}"
    )
    DATABASE_PARAMS = {}

engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
