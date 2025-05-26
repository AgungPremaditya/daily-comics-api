import os
from typing import Optional
from functools import lru_cache
from dotenv import load_dotenv
from supabase import create_client, Client
from .exceptions.database import DatabaseConnectionError
from .repositories.comic_repository import ComicRepository
from .repositories.panel_repository import PanelRepository

# Load environment variables
load_dotenv()

class SupabaseClient:
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create the Supabase client instance"""
        if cls._instance is None:
            supabase_url = os.environ.get("SUPABASE_URL")
            supabase_key = os.environ.get("SUPABASE_KEY")
            
            if not supabase_url or not supabase_key:
                raise DatabaseConnectionError("Missing Supabase credentials. Please check your .env file.")
            
            try:
                # Initialize client with URL and key only, without any additional options
                cls._instance = create_client(
                    supabase_url=supabase_url,
                    supabase_key=supabase_key
                )
            except Exception as e:
                raise DatabaseConnectionError(f"Failed to connect to Supabase: {str(e)}")
        
        return cls._instance

@lru_cache()
def get_supabase_client() -> Client:
    """Returns the Supabase client instance (cached)"""
    return SupabaseClient.get_client()

@lru_cache()
def get_comic_repository() -> ComicRepository:
    """Returns a ComicRepository instance (cached)"""
    return ComicRepository(get_supabase_client())

@lru_cache()
def get_panel_repository() -> PanelRepository:
    """Returns a PanelRepository instance (cached)"""
    return PanelRepository(get_supabase_client())