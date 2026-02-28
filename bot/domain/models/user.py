# bot/domain/models/user.py
from datetime import datetime, timezone
from typing import Optional

from bot.domain.models.user_role import UserRole

class User:
    def __init__(
        self,
        tg_id: int,
        name: Optional[str] = None,
        username: Optional[str] = None,
        language: Optional[str] = None,
        role: UserRole = UserRole.user,
        blocked: bool = False,
    ) -> None:

        if tg_id <= 0:
            raise ValueError("tg_id must be positive")

        now = datetime.now(timezone.utc)

        self._user_id: Optional[int] = None
        self._tg_id = tg_id
        self._name = name
        self._username = username
        self._language = language
        self._role = role
        self._blocked = blocked

    def update_profile(self, name: str | None, username: str | None) -> None:
        self._name = name
        self._username = username

    def block(self) -> None:
        self._blocked = True

    def unblock(self) -> None:
        self._blocked = False
