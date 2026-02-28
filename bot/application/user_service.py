# bot/application/user_service.py
import logging
logger = logging.getLogger('prehensor')

import telegram

from bot.infra.exceptions import DatabaseError
from bot.infra.repositories.user_repository import UserRepository
from bot.domain.models.user import User

class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.repo = user_repo
        self.user = None

    async def get_or_create_user(
            self,
            tg_user: telegram.User
        ) -> User:
        domain_user = None
        domain_user = await self.repo.get_by_telegram_id(tg_user.id)

        if domain_user is None:
            logger.info('[get_or_create_user] User not found, creating new one.')
            domain_user = User(
                tg_id=tg_user.id,
                name=tg_user.first_name,
                username=tg_user.username,
                language=tg_user.language_code,
            )
            await self.repo.save_or_update(domain_user)

        else:
            self.repo.mark_seen(domain_user._tg_id)

        return domain_user