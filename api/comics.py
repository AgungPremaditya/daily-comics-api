from fastapi import APIRouter, HTTPException, Depends
from typing import List
from db.supabase_client import get_supabase_client
from supabase import Client
from models.comic import Comic, ComicCreate, ComicUpdate

router = APIRouter(
    prefix="/comics",
    tags=["comics"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[Comic])
async def get_all_comics(supabase: Client = Depends(get_supabase_client)):
    """Get all comics"""
    response = supabase.table("comics").select("*").execute()
    
    if hasattr(response, 'error') and response.error:
        raise HTTPException(status_code=500, detail=f"Supabase error: {response.error.message}")
    
    return response.data

@router.get("/{comic_id}", response_model=Comic)
async def get_comic(comic_id: int, supabase: Client = Depends(get_supabase_client)):
    """Get a specific comic by ID"""
    response = supabase.table("comics").select("*").eq("id", comic_id).execute()
    
    if hasattr(response, 'error') and response.error:
        raise HTTPException(status_code=500, detail=f"Supabase error: {response.error.message}")
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Comic not found")
    
    return response.data[0]

@router.post("/", response_model=Comic)
async def create_comic(comic: ComicCreate, supabase: Client = Depends(get_supabase_client)):
    """Create a new comic"""
    response = supabase.table("comics").insert(comic.dict()).execute()
    
    if hasattr(response, 'error') and response.error:
        raise HTTPException(status_code=500, detail=f"Supabase error: {response.error.message}")
    
    return response.data[0]

@router.put("/{comic_id}", response_model=Comic)
async def update_comic(comic_id: int, comic: ComicUpdate, supabase: Client = Depends(get_supabase_client)):
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

@router.delete("/{comic_id}")
async def delete_comic(comic_id: int, supabase: Client = Depends(get_supabase_client)):
    """Delete a comic"""
    # First, check if the comic exists
    check_response = supabase.table("comics").select("*").eq("id", comic_id).execute()
    
    if not check_response.data:
        raise HTTPException(status_code=404, detail="Comic not found")
    
    # If it exists, delete it
    response = supabase.table("comics").delete().eq("id", comic_id).execute()
    
    if hasattr(response, 'error') and response.error:
        raise HTTPException(status_code=500, detail=f"Supabase error: {response.error.message}")
    
    return {"message": "Comic deleted successfully", "id": comic_id}