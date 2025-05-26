class DatabaseError(Exception):
    """Base exception for database errors"""
    pass

class RecordNotFoundError(DatabaseError):
    """Exception raised when a record is not found"""
    pass

class DatabaseConnectionError(DatabaseError):
    """Exception raised when there's an issue connecting to the database"""
    pass

class ValidationError(DatabaseError):
    """Exception raised when there's a validation error"""
    pass 