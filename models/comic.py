from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class Panel(BaseModel):
    """Model for a comic panel"""
    id: Optional[int] = None
    comic_id: Optional[int] = None
    sentence: str
    image_url: str  # Changed from imageUrl for consistency
    panel_order: int
    
    class Config:
        orm_mode = True

class ComicBase(BaseModel):
    """Base model for comics"""
    date: date
    title: str

class ComicCreate(ComicBase):
    """Model for creating a new comic"""
    pass

class ComicUpdate(BaseModel):
    """Model for updating an existing comic"""
    date: Optional[date] = None
    title: Optional[str] = None

class Comic(ComicBase):
    """Model for a comic with ID"""
    id: int
    panels: List[Panel] = []
    
    class Config:
        orm_mode = True