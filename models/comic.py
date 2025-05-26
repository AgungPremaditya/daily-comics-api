from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from .story import Story 

class Panel(BaseModel):
    """Model for a comic panel"""
    id: Optional[int] = None
    comic_id: Optional[int] = None
    sentence: str
    image_url: str  
    panel_order: int
    
    model_config = {
        "from_attributes": True
    }

class ComicBase(BaseModel):
    """Base model for comics"""
    date: date
    title: str
    story_id: int  # Required story reference

class ComicCreate(ComicBase):
    """Model for creating a new comic"""
    pass

class ComicUpdate(BaseModel):
    """Model for updating an existing comic"""
    date: Optional[date] = None
    title: Optional[str] = None
    story_id: Optional[int] = None

class Comic(ComicBase):
    """Model for a comic with ID"""
    id: int
    panels: List[Panel] = []
    story: Story  # Required story relationship
    
    model_config = {
        "from_attributes": True
    }