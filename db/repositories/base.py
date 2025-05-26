from typing import Any, Dict, List, Optional, TypeVar, Generic
from supabase import Client
from ..exceptions.database import DatabaseError, RecordNotFoundError

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, supabase: Client, table_name: str):
        self.supabase = supabase
        self.table_name = table_name

    def _handle_error(self, response: Any) -> None:
        """Handle common Supabase errors"""
        if hasattr(response, 'error') and response.error:
            raise DatabaseError(f"Supabase error: {response.error.message}")

    async def find_all(self) -> List[Dict[str, Any]]:
        """Get all records from the table"""
        response = self.supabase.table(self.table_name).select("*").execute()
        self._handle_error(response)
        return response.data

    async def find_by_id(self, id: int) -> Dict[str, Any]:
        """Get a record by ID"""
        response = self.supabase.table(self.table_name).select("*").eq("id", id).execute()
        self._handle_error(response)
        
        if not response.data:
            raise RecordNotFoundError(f"{self.table_name} with ID {id} not found")
        
        return response.data[0]

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record"""
        response = self.supabase.table(self.table_name).insert(data).execute()
        self._handle_error(response)
        return response.data[0]

    async def update(self, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record"""
        response = self.supabase.table(self.table_name).update(data).eq("id", id).execute()
        self._handle_error(response)
        
        if not response.data:
            raise RecordNotFoundError(f"{self.table_name} with ID {id} not found")
        
        return response.data[0]

    async def delete(self, id: int) -> None:
        """Delete a record"""
        response = self.supabase.table(self.table_name).delete().eq("id", id).execute()
        self._handle_error(response)
        
        if not response.data:
            raise RecordNotFoundError(f"{self.table_name} with ID {id} not found") 