# bot/infra/repositories/sqlite_user_repository.py
from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import select, update, func
from sqlalchemy.dialects.sqlite import insert

from bot.infra.repositories.user_repository import UserRepository
from bot.infra.db import async_session
from bot.infra.db.models.user_orm import UserORM
from bot.domain.models.user_role import UserRole
from bot.domain.models.user import User
from bot.infra.exceptions import ORMUserNotFound

class SqliteUserRepository(UserRepository):

    async def get_by_telegram_id(self, tg_id: int) -> Optional[User]:
        stmt = select(UserORM).where(UserORM.tg_id == tg_id)

        async with async_session() as session:
            result = await session.execute(stmt)
            orm_user = result.scalar_one_or_none()

        if orm_user is None:
            return None

        return self._to_domain(orm_user)

    async def save_or_update(self, domain_user: User) -> None:
        now = datetime.now(timezone.utc)

        stmt = insert(UserORM).values(
            tg_id=domain_user._tg_id,
            name=domain_user._name,
            username=domain_user._username,
            language=domain_user._language,
            role=domain_user._role.value,
            blocked=domain_user._blocked,
            last_seen=now,
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=["tg_id"],
            set_={
                "name": domain_user._name,
                "username": domain_user._username,
                "language": domain_user._language,
                "role": domain_user._role.value,
                "blocked": domain_user._blocked,
                # На server-default не рассчитываем, обновляем вручную
                "updated_at": func.now(),
            },
        )
        async with async_session() as session:
            async with session.begin():
                await session.execute(stmt)

    async def mark_seen(self, tg_id: int) -> None:
        async with async_session() as session:
            async with session.begin():

                stmt = (
                    update(UserORM)
                    .where(UserORM.tg_id == tg_id)
                    .values(last_seen=func.now())
                )

                result = await session.execute(stmt)

                if result.rowcount == 0:
                    raise ORMUserNotFound(f"user tg_id={tg_id} not found")

    def _to_domain(self, orm: UserORM) -> User:
        return User(
            tg_id=orm.tg_id,
            name=orm.name,
            username=orm.username,
            language=orm.language,
            # Долг: проверить на валидность
            role=UserRole(orm.role),
            blocked=orm.blocked,
        )
