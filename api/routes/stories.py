from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from db.supabase_client import get_supabase_client
from supabase import Client
from models.story import Story, StoryCreate, StoryResponse, StoryList
from api.services.story_service import StoryService
from datetime import datetime

router = APIRouter(
    prefix="/stories",
    tags=["stories"],
    responses={404: {"description": "Not found"}}
)

@router.post("/generate", response_model=StoryResponse)
async def generate_story(
    prompt: str = "",
    story_service: StoryService = Depends(StoryService),
    supabase: Client = Depends(get_supabase_client)
):
    """Generate a new story using OpenAI and save it to the database.
    Note: The prompt parameter is ignored as we use a fixed prompt for consistency."""
    return await story_service.generate_and_save_story(prompt, supabase)

@router.get("/", response_model=StoryList)
async def list_stories(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by title"),
    story_service: StoryService = Depends(StoryService),
    supabase: Client = Depends(get_supabase_client)
):
    """List stories with pagination and search"""
    return await story_service.list_stories(page, page_size, search, supabase)

@router.get("/{story_id}", response_model=StoryResponse)
async def get_story(
    story_id: int,
    story_service: StoryService = Depends(StoryService),
    supabase: Client = Depends(get_supabase_client)
):
    """Get story details by ID"""
    return await story_service.get_story_by_id(story_id, supabase) 