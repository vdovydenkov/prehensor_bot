# bot/domain/models/role_permission.py
from bot.domain.models.user_role import UserRole
from bot.domain.models.permissions import Permission

ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
    UserRole.USER: {
        Permission.DOWNLOAD_MATERIALS,
    },
    UserRole.POWER_USER: {
        Permission.DOWNLOAD_MATERIALS,
        Permission.VIEW_BASIC_STATS,
    },
    UserRole.ADMIN: {
        Permission.DOWNLOAD_MATERIALS,
        Permission.VIEW_BASIC_STATS,
        Permission.VIEW_DETAILED_STATS,
        Permission.MANAGE_USERS,
    },
    UserRole.OWNER: set(Permission),  # всё
}