# bot/infra/db/models/user_orm.py
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from bot.infra.db import Base

class UserORM(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        Integer,
        autoincrement=True,
        primary_key=True
    )

    tg_id: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        index=True,
        nullable=False
    )

    last_chat_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    name: Mapped[str | None] = mapped_column(
        String(255)
    )
    username: Mapped[str | None] = mapped_column(
        String(255)
    )
    language: Mapped[str | None] = mapped_column(
        String(10)
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    blocked: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )
