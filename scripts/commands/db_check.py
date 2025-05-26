import logging
from typing import Optional, List
from datetime import date
from db import get_comic_repository, get_panel_repository
from ..utils.common import format_comic_output, parse_date

logger = logging.getLogger(__name__)

async def list_comics() -> None:
    """List all comics in the database"""
    comic_repo = get_comic_repository()
    comics = await comic_repo.find_all()
    
    if not comics:
        logger.info("No comics found in the database.")
        return
    
    logger.info(f"Found {len(comics)} comics:")
    for comic in comics:
        # Get panels for this comic
        panels = await get_panel_repository().find_by_comic_id(comic['id'])
        comic['panels'] = panels
        logger.info("\n" + format_comic_output(comic, include_panels=False))
        logger.info(f"Panels: {len(panels)}")
        logger.info("-" * 40)

async def get_comic_by_id(comic_id: int) -> Optional[dict]:
    """Get a specific comic by ID"""
    try:
        comic = await get_comic_repository().find_with_panels(comic_id)
        logger.info("\n" + format_comic_output(comic))
        return comic
    except Exception as e:
        logger.error(f"Error getting comic {comic_id}: {e}")
        return None

async def get_comics_by_date(target_date: Optional[str] = None) -> List[dict]:
    """Get comics for a specific date"""
    date_obj = parse_date(target_date)
    try:
        comics = await get_comic_repository().find_by_date(date_obj.isoformat())
        
        if not comics:
            logger.info(f"No comics found for date {date_obj.isoformat()}")
            return []
        
        logger.info(f"Found {len(comics)} comics for date {date_obj.isoformat()}:")
        for comic in comics:
            logger.info(f"ID: {comic['id']}, Title: {comic['title']}")
        
        return comics
    except Exception as e:
        logger.error(f"Error getting comics for date {date_obj.isoformat()}: {e}")
        return []

async def insert_test_comic() -> Optional[int]:
    """Insert a test comic into the database"""
    try:
        comic_repo = get_comic_repository()
        panel_repo = get_panel_repository()
        
        # Create comic data
        comic_data = {
            "date": date.today().isoformat(),
            "title": "Test Comic"
        }
        
        # Create panels data
        panels_data = [
            {
                "sentence": "This is the first panel of a test comic.",
                "image_url": "https://example.com/image1.jpg",
                "panel_order": 1
            },
            {
                "sentence": "This is the second panel of a test comic.",
                "image_url": "https://example.com/image2.jpg",
                "panel_order": 2
            }
        ]
        
        # Create comic with panels
        comic = await comic_repo.create_with_panels(comic_data, panels_data)
        logger.info(f"Successfully inserted test comic with ID: {comic['id']} and {len(panels_data)} panels")
        return comic['id']
        
    except Exception as e:
        logger.error(f"Error inserting test comic: {e}")
        return None 