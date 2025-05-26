from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class StoryBase(BaseModel):
    """Base model for stories"""
    title: str
    story: str

class StoryCreate(StoryBase):
    """Model for creating a new story"""
    pass

class Story(StoryBase):
    """Model for a story with ID and timestamps"""
    id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = {
        "from_attributes": True
    }

class StoryResponse(Story):
    """Response model for story details"""
    pass

class StoryBrief(BaseModel):
    """Brief story information for listing"""
    id: int
    title: str
    created_at: datetime
    
    model_config = {
        "from_attributes": True
    }

class StoryList(BaseModel):
    """Paginated list of stories"""
    items: List[StoryBrief]
    total: int
    page: int
    page_size: int
    total_pages: int