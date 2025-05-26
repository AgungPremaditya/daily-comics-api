from typing import List
from fastapi import HTTPException
from supabase import Client
from models.comic import Comic, ComicCreate, ComicUpdate
from api.integrations.openai_integration import generate_story, generate_comic_panels
from datetime import date

class ComicService:
    async def get_all_comics(self, supabase: Client) -> List[Comic]:
        """Get all comics from the database"""
        response = supabase.table("comics").select("*").execute()
        
        if hasattr(response, 'error') and response.error:
            raise HTTPException(status_code=500, detail=f"Supabase error: {response.error.message}")
        
        return response.data

    async def get_comic_by_id(self, comic_id: int, supabase: Client) -> Comic:
        """Get a specific comic by ID"""
        response = supabase.table("comics").select("*").eq("id", comic_id).execute()
        
        if hasattr(response, 'error') and response.error:
            raise HTTPException(status_code=500, detail=f"Supabase error: {response.error.message}")
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Comic not found")
        
        return response.data[0]

    async def create_comic(self, comic: ComicCreate, supabase: Client) -> Comic:
        """Create a new comic"""
        response = supabase.table("comics").insert(comic.dict()).execute()
        
        if hasattr(response, 'error') and response.error:
            raise HTTPException(status_code=500, detail=f"Supabase error: {response.error.message}")
        
        return response.data[0]

    async def update_comic(self, comic_id: int, comic: ComicUpdate, supabase: Client) -> Comic:
        """Update an existing comic"""
        # Remove None values from the update dict
        update_data = {k: v for k, v in comic.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")
        
        response = supabase.table("comics").update(update_data).eq("id", comic_id).execute()
        
        if hasattr(response, 'error') and response.error:
            raise HTTPException(status_code=500, detail=f"Supabase error: {response.error.message}")
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Comic not found")
        
        return response.data[0]

    async def generate_comic(self, prompt: str, supabase: Client) -> Comic:
        """Generate a new comic story and store it in Supabase"""
        # Generate story with 6 sentences
        title, sentences = generate_story(prompt)
        
        if len(sentences) != 6:
            raise HTTPException(status_code=500, detail="Failed to generate exactly 6 sentences")
        
        # Create comic in database
        comic_data = {
            "title": title,
            "date": date.today().isoformat()
        }
        
        # Insert comic
        comic_response = supabase.table("comics").insert(comic_data).execute()
        
        if hasattr(comic_response, 'error') and comic_response.error:
            raise HTTPException(status_code=500, detail=f"Supabase error: {comic_response.error.message}")
        
        if not comic_response.data:
            raise HTTPException(status_code=500, detail="Failed to create comic")
        
        comic_id = comic_response.data[0]['id']
        
        # Create panels with just the sentences (no images)
        panels = []
        for i, sentence in enumerate(sentences):
            panel = {
                "comic_id": comic_id,
                "sentence": sentence,
                "image_url": "",  # Empty image URL since we're not generating images
                "panel_order": i + 1
            }
            panels.append(panel)
        
        # Insert panels
        panels_response = supabase.table("panels").insert(panels).execute()
        
        if hasattr(panels_response, 'error') and panels_response.error:
            # If panels insertion fails, delete the comic to avoid orphaned records
            supabase.table("comics").delete().eq("id", comic_id).execute()
            raise HTTPException(status_code=500, detail=f"Supabase error: {panels_response.error.message}")
        
        # Get the complete comic with panels
        result = comic_response.data[0]
        result["panels"] = panels_response.data
        
        return result 