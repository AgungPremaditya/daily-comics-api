"""API package for Daily Comics"""

from .main import app
from .routes.comics import router as comics_router

__all__ = ['app', 'comics_router']