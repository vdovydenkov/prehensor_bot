# bot/infra/db/__init__.py
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase

from bot.config.constants import DB_URL

engine = create_async_engine(
    DB_URL,
    echo=False,
)

alembic_url = DB_URL.replace("+aiosqlite", "")
alembic_engine = create_engine(
    alembic_url,
    echo=False,
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass