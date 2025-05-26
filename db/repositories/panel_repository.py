from typing import Dict, List, Any
from supabase import Client
from .base import BaseRepository
from models.comic import Panel

class PanelRepository(BaseRepository[Panel]):
    def __init__(self, supabase: Client):
        super().__init__(supabase, "panels")

    async def find_by_comic_id(self, comic_id: int) -> List[Dict[str, Any]]:
        """Get all panels for a specific comic"""
        response = self.supabase.table(self.table_name).select("*").eq("comic_id", comic_id).order("panel_order").execute()
        self._handle_error(response)
        return response.data

    async def update_panel_order(self, panel_id: int, new_order: int) -> Dict[str, Any]:
        """Update the order of a panel"""
        response = self.supabase.table(self.table_name).update({"panel_order": new_order}).eq("id", panel_id).execute()
        self._handle_error(response)
        return response.data[0]

    async def bulk_create(self, panels: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create multiple panels at once"""
        response = self.supabase.table(self.table_name).insert(panels).execute()
        self._handle_error(response)
        return response.data 