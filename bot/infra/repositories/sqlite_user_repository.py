# bot/infra/repositories/sqlite_user_repository.py
import logging
logger = logging.getLogger('prehensor')

from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import select, update, func
from sqlalchemy.dialects.sqlite import insert

from bot.infra.repositories.user_repository import UserRepository
from bot.infra.db import async_session
from bot.infra.db.models.user_orm import UserORM
from bot.domain.models.user_role import UserRole
from bot.domain.models.user import DomainUser
from bot.infra.exceptions import ORMUserNotFound

class SqliteUserRepository(UserRepository):

    async def get_by_telegram_id(self, tg_id: int) -> Optional[DomainUser]:
        stmt = select(UserORM).where(UserORM.tg_id == tg_id)

        async with async_session() as session:
            result = await session.execute(stmt)
            orm_user = result.scalar_one_or_none()

        if orm_user is None:
            return None

        return self._to_domain(orm_user)

    async def save_or_update(self, domain_user: DomainUser) -> None:
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

    async def get_all_users(self) -> list[DomainUser]:
        stmt = select(UserORM)

        async with async_session() as session:
            result = await session.execute(stmt)
            orm_users = result.scalars().all()

            return [self._to_domain(u) for u in orm_users]

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

    def _to_domain(self, orm: UserORM) -> DomainUser:
        role_value = orm.role
        if role_value not in UserRole._value2member_map_:
            logger.warning("[_to_domain] Corrupted role detected, auto-fix to USER")
            self._fix_role(
                user_id=orm.user_id, 
                default_role=UserRole.USER,
            )
            role_value = UserRole.USER.value
        return DomainUser(
            tg_id=orm.tg_id,
            name=orm.name,
            username=orm.username,
            language=orm.language,
            role=UserRole(role_value),
            blocked=orm.blocked,
        )

    async def _fix_role(self, user_id: int, default_role: UserRole) -> None:
        async with async_session() as session:
            async with session.begin():

                stmt = (
                    update(UserORM)
                    .where(UserORM.user_id == user_id)
                    .values(
                        role=default_role.value,
                    )
                )

                result = await session.execute(stmt)

                if result.rowcount == 0:
                    raise ORMUserNotFound(f"user id={user_id} not found during role fix")

        logger.warning(
            f"[fix_role] Role auto-corrected to '{default_role.value}' "
            f"for user_id={user_id}"
        )