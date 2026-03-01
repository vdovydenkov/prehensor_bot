# bot/domain/models/user_roles.py
from enum import Enum, auto

class UserRole(Enum):
    USER       = 'user'
    POWER_USER = 'power_user'
    ADMIN      = 'admin'
    OWNER      = 'owner'
