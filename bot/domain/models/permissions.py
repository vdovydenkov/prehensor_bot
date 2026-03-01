# bot/domain/models/permissions.py
from enum import Enum, auto

class Permission(Enum):
    DOWNLOAD_MATERIALS  = auto()
    VIEW_BASIC_STATS    = auto()
    VIEW_DETAILED_STATS = auto()
    MANAGE_USERS        = auto()