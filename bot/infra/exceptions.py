# bot/infra/exceptions.py

class DatabaseError(Exception):
    pass

class RepositoryError(DatabaseError):
    pass

class ORMError(DatabaseError):
    pass

class ORMUserNotFound(ORMError):
    pass

class ORMUserAlreadyExists(ORMError):
    pass

class ORMUserRoleValueError(ORMError):
    pass