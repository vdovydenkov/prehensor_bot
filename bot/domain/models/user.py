# bot/domain/models/user.py
from typing import Optional

from bot.domain.models.user_role import UserRole
from bot.domain.models.permissions import Permission
from bot.domain.models.role_permission import ROLE_PERMISSIONS

class DomainUser:
    def __init__(
        self,
        tg_id:        int,
        last_chat_id: Optional[int] = None,
        name:         Optional[str] = None,
        username:     Optional[str] = None,
        language:     Optional[str] = None,
        role:         UserRole = UserRole.USER,
        blocked:      bool = False,
    ) -> None:

        if tg_id <= 0:
            raise ValueError("tg_id must be positive")

        self._user_id: Optional[int] = None
        self._tg_id = tg_id
        self._last_chat_id: Optional[int] = None
        self._name = name
        self._username = username
        self._language = language
        self._role = role
        self._blocked = blocked

    @property
    def tg_id(self) -> int:
        return self._tg_id

    @tg_id.setter
    def tg_id(self, value: int) -> None:
        self._tg_id = value

    @property
    def last_chat_id(self) -> int:
        return self._last_chat_id

    @last_chat_id.setter
    def last_chat_id(self, value: int) -> None:
        self._tg_id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = value


    @property
    def role(self) -> UserRole:
        return self._role

    @role.setter
    def role(self, value: UserRole):
        self._role = value

    @property
    def blocked(self) -> bool:
        return self._blocked

    @blocked.setter
    def blocked(self, value: bool):
        # Избежать блокировки владельца
        if value and self.is_owner():
            return
        self._blocked = value

    @property
    def is_owner(self) -> bool:
        return self._role == UserRole.OWNER

    def block(self) -> None:
        # Избежать блокировки владельца
        if self.is_owner():
            return
        self._blocked = True

    def unblock(self) -> None:
        self._blocked = False

    def has_permission(self, permission: Permission) -> bool:
        return permission in ROLE_PERMISSIONS[self.role]
