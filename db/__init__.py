"""Database layer for the application"""

from .supabase_client import (
    get_supabase_client,
    get_comic_repository,
    get_panel_repository
)
from .exceptions.database import (
    DatabaseError,
    RecordNotFoundError,
    DatabaseConnectionError,
    ValidationError
)

__all__ = [
    'get_supabase_client',
    'get_comic_repository',
    'get_panel_repository',
    'DatabaseError',
    'RecordNotFoundError',
    'DatabaseConnectionError',
    'ValidationError'
]