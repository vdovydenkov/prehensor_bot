# bot/presentation/list_formater.py
from bot.domain.models.user import DomainUser
from bot.presentation.common.exceptions import PresentationLayerError
import logging
logger = logging.getLogger('prehensor')


def format_list(users: list[DomainUser]) -> str:
    '''Принимает список domain User,
    Возвращает строку, пригодную для вывода пользователю.
    '''
    formatted_users = [
        (
            f"{u.name} [{u.username}:{u.tg_id}]\n"
            f"  Role:{u.role.value}, blocked:{u.blocked}, language:{u.language}\n"
        )
        for u in users
    ]

    counter = len(formatted_users)

    if counter == 0:
        raise PresentationLayerError("format_list: list is empty or invalid.")

    body = "\n".join(formatted_users)

    return (
        f"{counter} пользователей.\n"
         "\n\n"
        f"{body}"
    )
