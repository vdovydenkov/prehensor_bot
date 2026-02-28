# bot/infra/exceptions.py

class DatabaseError(Exception):
    '''
    Base exception for all database-related errors.
    '''
    pass

class RepositoryError(DatabaseError):
    '''
    Base repository exception.
    '''
    pass

class ORMError(DatabaseError):
    '''
    Wrapper for SQLAlchemy / ORM exceptions.
    '''
    pass

class ORMUserNotFound(ORMError):
    pass

class ORMUserAlreadyExists(ORMError):
    pass