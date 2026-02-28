# bot/domain/models/user_roles.py
from enum import Enum

class UserRole(Enum):
    user  = 'user'
    admin = 'admin'
