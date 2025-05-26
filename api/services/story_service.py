from typing import Optional
from fastapi import HTTPException
from supabase import Client
from models.story import Story, StoryCreate, StoryList, StoryBrief
from api.integrations.openai_integration import generate_story
import math

class StoryService:
    # Fixed prompt for story generation
    STORY_PROMPT = """Write a story in 7 sentences. The first sentence is the title of the story (not in quotes). The story must be written as one single paragraph. Use simple words that children can understand. The story should be about two strangers who meet in a very specific and unusual place (for example: a parking lot during a balloon festival, a library during a fire drill, or a zoo on a rainy Monday). Something small but surprising should happen — maybe they share a snack, help each other, or make a funny mistake. The story should end with a feeling — either happy, sad, or inspired — and should never repeat the same characters, place, or surprise."""

    async def generate_and_save_story(self, prompt: str, supabase: Client) -> Story:
        """Generate a story using OpenAI and save it to the database"""
        try:
            # Generate story using the fixed prompt
            title, sentences = generate_story(self.STORY_PROMPT)
            
            # Remove any quotes from the title
            title = title.strip('"').strip()
            
            # Join the remaining sentences into the story text
            story_text = ". ".join(sentences[1:])
            if not story_text.endswith('.'):
                story_text += "."
            
            # Prepare story data
            story_data = {
                "title": title,
                "story": story_text
            }
            
            # Save to database
            response = supabase.table("story").insert(story_data).execute()
            
            if hasattr(response, 'error') and response.error:
                raise HTTPException(status_code=500, detail=f"Supabase error: {response.error.message}")
            
            return response.data[0]
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to generate and save story: {str(e)}")

    async def list_stories(
        self, 
        page: int, 
        page_size: int, 
        search: Optional[str],
        supabase: Client
    ) -> StoryList:
        """List stories with pagination and search"""
        try:
            # Start building the query
            query = supabase.table("story").select("id, title, created_at", count="exact")
            
            # Add search if provided
            if search:
                query = query.ilike("title", f"%{search}%")
            
            # Add pagination
            start = (page - 1) * page_size
            query = query.range(start, start + page_size - 1).order("created_at", desc=True)
            
            # Execute query
            response = query.execute()
            
            if hasattr(response, 'error') and response.error:
                raise HTTPException(status_code=500, detail=f"Supabase error: {response.error.message}")
            
            # Calculate pagination info
            total = response.count
            total_pages = math.ceil(total / page_size)
            
            return StoryList(
                items=response.data,
                total=total,
                page=page,
                page_size=page_size,
                total_pages=total_pages
            )
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to list stories: {str(e)}")

    async def get_story_by_id(self, story_id: int, supabase: Client) -> Story:
        """Get a story by ID"""
        try:
            response = supabase.table("story").select("*").eq("id", story_id).execute()
            
            if hasattr(response, 'error') and response.error:
                raise HTTPException(status_code=500, detail=f"Supabase error: {response.error.message}")
            
            if not response.data:
                raise HTTPException(status_code=404, detail="Story not found")
            
            return response.data[0]
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get story: {str(e)}") 