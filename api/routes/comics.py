from fastapi import APIRouter, HTTPException, Depends
from typing import List
from db.supabase_client import get_supabase_client
from supabase import Client
from models.comic import Comic, ComicCreate, ComicUpdate
from api.services.comic_service import ComicService
from datetime import date

router = APIRouter(
    prefix="/comics",
    tags=["comics"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Comic])
async def get_all_comics(
    comic_service: ComicService = Depends(ComicService),
    supabase: Client = Depends(get_supabase_client)
):
    """Get all comics"""
    return await comic_service.get_all_comics(supabase)

@router.get("/{comic_id}", response_model=Comic)
async def get_comic(
    comic_id: int, 
    comic_service: ComicService = Depends(ComicService),
    supabase: Client = Depends(get_supabase_client)
):
    """Get a specific comic by ID"""
    return await comic_service.get_comic_by_id(comic_id, supabase)

@router.post("/", response_model=Comic)
async def create_comic(
    comic: ComicCreate,
    comic_service: ComicService = Depends(ComicService),
    supabase: Client = Depends(get_supabase_client)
):
    """Create a new comic"""
    return await comic_service.create_comic(comic, supabase)

@router.put("/{comic_id}", response_model=Comic)
async def update_comic(
    comic_id: int,
    comic: ComicUpdate,
    comic_service: ComicService = Depends(ComicService),
    supabase: Client = Depends(get_supabase_client)
):
    """Update an existing comic"""
    return await comic_service.update_comic(comic_id, comic, supabase)

@router.post("/generate", response_model=Comic)
async def generate_comic(
    prompt: str = "Create a short funny comic story, with 6 sentences",
    comic_service: ComicService = Depends(ComicService),
    supabase: Client = Depends(get_supabase_client)
):
    """Generate a new comic story and store it in Supabase"""
    return await comic_service.generate_comic(prompt, supabase) 