# bot/infra/repositories/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional

from bot.domain.models.user import DomainUser


class UserRepository(ABC):

    @abstractmethod
    async def get_by_telegram_id(self, tg_id: int) -> Optional[DomainUser]:
        pass

    @abstractmethod
    async def save_or_update(self, domain_user: DomainUser) -> None:
        pass

    @abstractmethod
    async def get_all_users(self) -> list[DomainUser]:
        pass

    @abstractmethod
    async def mark_seen(self, tg_id: int) -> None:
        pass

