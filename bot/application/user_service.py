# bot/application/user_service.py
import telegram
from sqlalchemy.exc import SQLAlchemyError
from collections.abc import Sequence

from bot.config.constants import (
    MAX_ROLE_LENGTH,
    MIN_ROLE_LENGTH,
)

from bot.infra.repositories.user_repository import UserRepository
from bot.domain.models.user import DomainUser
from bot.domain.models.user_role import UserRole
from bot.domain.models.permissions import Permission
from bot.application.exceptions import (
    UserServiceError,
    UserNotFoundError,
    UserBlockedError,
    AccessDeniedError,
    RoleNotFoundError,
)

import logging
logger = logging.getLogger('prehensor')


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.repo = user_repo

    async def get_user_by_id(
        self,
        tg_id: int,
    ) -> DomainUser:
        return await self.repo.get_by_telegram_id(tg_id)

    async def create_user(
        self,
        tg_user: telegram.User
    ) -> DomainUser:
        local_id = 'UserService.create_user'

        domain_user = None
        domain_user = await self.get_user_by_id(tg_user.id)

        if domain_user:
            logger.info(
                '[%s] User (%s:%s) already exists.',
                local_id,
                domain_user.name,
                domain_user.tg_id,
            )
            return domain_user

        logger.info(f'[{local_id}] User not found, creating new one.')

        domain_user = DomainUser(
            tg_id=tg_user.id,
            name=tg_user.first_name,
            username=tg_user.username,
            language=tg_user.language_code,
        )

        await self.repo.save_or_update(domain_user)

        logger.info(
            f'[{local_id}] User successfuly created: "%s":%s',
            domain_user.name,
            domain_user.tg_id,
        )

        return domain_user
    
    async def list_users(
        self,
        requesting_user: DomainUser
    ) -> list[DomainUser]:
        '''Возвращает список зарегистрированных пользователей.
        Параметр: Телеграм-идентификатор пользователя

        0) берет из БД пользователя, запросившего список,
        1) Проверяет,
        2) запрашивает список пользователей из репозитория;
        3) проверяет и фильтрует список.
        '''
        self._check_user(
            requesting_user,
            [Permission.VIEW_DETAILED_STATS]
        )

        local_id = 'list_users'
        
        try:
            users = await self.repo.get_all_users()
        except SQLAlchemyError as e:
            msg = str(e)
            logger.warning(f'[{local_id}] Infrastructure error:\n{msg}')
            raise UserServiceError('Failed to retrieve user list.')
        
        filtered_users = [
            u for u in users
            if isinstance(u, DomainUser)
        ]

        return filtered_users

    async def set_as_owner(
        self,
        user: DomainUser
    ) -> None:
        '''Отдельный метод для установки прав владельца.'''
        self._check_user(user)

        if user.is_owner:
            return

        user.role = UserRole.OWNER

        await self.repo.save_or_update(user)

    async def set_role(
        self,
        user: DomainUser | None,
        target_role: str
    ) -> UserRole:
        '''Устанавливает заданную роль переданному пользователю.
        Роль OWNER игнорируется.
        '''

        self._check_user(
            user,
            [Permission.MANAGE_USERS],
        )

        role_length = len(target_role)
        if role_length < MIN_ROLE_LENGTH or role_length > MAX_ROLE_LENGTH:
            raise RoleNotFoundError(
                f'Role length ({role_length}) '
                f'is out of range [{MIN_ROLE_LENGTH}..{MAX_ROLE_LENGTH}].'
            )

        try:
            new_role = UserRole[target_role]
        except KeyError:
            raise RoleNotFoundError(
                f'Role "{target_role}" not found ({user.name}:{user.tg_id}).'
            )

        if new_role == UserRole.OWNER:
            raise RoleNotFoundError(
                'Tried to set owner role.'
            )

        user.role = new_role
        await self.repo.save_or_update(user)

        return user.role
        
    def _check_user(
        self,
        user: DomainUser | None,
        # Если права не заданы, проверка будет пройдена с положительным результатом
        required_permissions: Sequence[Permission] = [],
    ) -> None:
        '''Проверяет пользователя на блокировку и права.
        Параметры: доменный пользователь, список требуемых прав.

        1) сначала просто на None,
        2) если владелец — дальше не проверяем,
        3) на блокировку,
        4) на все перечисленные права.

        Бросает исключения в соответствии с проблемой.
        '''
        if user is None:
            raise UserNotFoundError('User is empty.')
        if user.is_owner:
            return
        if user.blocked:
            raise UserBlockedError(
                f'User (Telegram id = {user.tg_id}) is blocked.'
            )
        for perm in required_permissions:
            if not user.has_permission(perm):
                raise AccessDeniedError(
                    f'{user.role.value} {user.name} (id={user.tg_id}) '
                    f'has no permission: {perm}.'
                )
