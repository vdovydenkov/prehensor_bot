# bot/application/exceptions.py

class UserServiceError(Exception):
    pass

class AccessDeniedError(UserServiceError):
    pass

class UserBlockedError(AccessDeniedError):
    pass

class UserNotFoundError(UserServiceError):
    pass
