from typing import Dict, List, Any
from supabase import Client
from .base import BaseRepository
from models.comic import Comic, ComicCreate, ComicUpdate

class ComicRepository(BaseRepository[Comic]):
    def __init__(self, supabase: Client):
        super().__init__(supabase, "comics")

    async def find_with_panels(self, comic_id: int) -> Dict[str, Any]:
        """Get a comic with its panels"""
        # First get the comic
        comic = await self.find_by_id(comic_id)
        
        # Then get its panels
        panels_response = self.supabase.table("panels").select("*").eq("comic_id", comic_id).order("panel_order").execute()
        self._handle_error(panels_response)
        
        # Combine the results
        comic["panels"] = panels_response.data
        return comic

    async def find_by_date(self, date: str) -> List[Dict[str, Any]]:
        """Find comics by date"""
        response = self.supabase.table(self.table_name).select("*").eq("date", date).execute()
        self._handle_error(response)
        return response.data

    async def create_with_panels(self, comic_data: Dict[str, Any], panels_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create a comic with its panels in a transaction"""
        # First create the comic
        comic = await self.create(comic_data)
        comic_id = comic["id"]
        
        try:
            # Add comic_id to each panel
            for panel in panels_data:
                panel["comic_id"] = comic_id
            
            # Create the panels
            panels_response = self.supabase.table("panels").insert(panels_data).execute()
            self._handle_error(panels_response)
            
            # Combine the results
            comic["panels"] = panels_response.data
            return comic
            
        except Exception as e:
            # If panels creation fails, delete the comic to maintain consistency
            await self.delete(comic_id)
            raise e 