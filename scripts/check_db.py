import sys
import os

# Add the project root to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.supabase_client import get_supabase_client
from models.comic import Comic
from datetime import date
import json

# Get the Supabase client
supabase = get_supabase_client()

def insert_test_comic():
    """Insert a test comic into the database"""
    # First, insert the comic
    comic_data = {
        "date": date.today().isoformat(),
        "title": "Test Comic"
    }
    
    comic_response = supabase.table('comics').insert(comic_data).execute()
    
    if not comic_response.data:
        print("Failed to insert comic")
        return None
    
    comic_id = comic_response.data[0]['id']
    
    # Then, insert the panels
    panels_data = [
        {
            "comic_id": comic_id,
            "sentence": "This is the first panel of a test comic.",
            "image_url": "https://example.com/image1.jpg",
            "panel_order": 1
        },
        {
            "comic_id": comic_id,
            "sentence": "This is the second panel of a test comic.",
            "image_url": "https://example.com/image2.jpg",
            "panel_order": 2
        }
    ]
    
    panels_response = supabase.table('panels').insert(panels_data).execute()
    
    if panels_response.data:
        print(f"Successfully inserted test comic with ID: {comic_id} and {len(panels_data)} panels")
    else:
        print("Failed to insert panels")
    
    return comic_id

def list_comics():
    """List all comics in the database"""
    response = supabase.table('comics').select('*').execute()
    
    if not response.data:
        print("No comics found in the database.")
        return
    
    print(f"Found {len(response.data)} comics:")
    for comic in response.data:
        # Get panels for this comic
        panels_response = supabase.table('panels').select('*').eq('comic_id', comic['id']).order('panel_order').execute()
        panels = panels_response.data if panels_response.data else []
        
        print(f"ID: {comic['id']}, Title: {comic['title']}, Date: {comic['date']}")
        print(f"Panels: {len(panels)}")
        print("-" * 40)

def get_comic_by_id(comic_id):
    """Get a specific comic by ID"""
    comic_response = supabase.table('comics').select('*').eq('id', comic_id).execute()
    
    if not comic_response.data:
        print(f"No comic found with ID {comic_id}")
        return
    
    comic = comic_response.data[0]
    
    # Get panels for this comic
    panels_response = supabase.table('panels').select('*').eq('comic_id', comic_id).order('panel_order').execute()
    panels = panels_response.data if panels_response.data else []
    
    print(f"Comic ID: {comic['id']}")
    print(f"Title: {comic['title']}")
    print(f"Date: {comic['date']}")
    print("Panels:")
    for i, panel in enumerate(panels, 1):
        print(f"  Panel {i}:")
        print(f"    Sentence: {panel['sentence']}")
        print(f"    Image URL: {panel['image_url']}")
    
    # Combine comic and panels
    comic['panels'] = panels
    return comic

def get_comics_by_date(target_date):
    """Get comics for a specific date"""
    response = supabase.table('comics').select('*').eq('date', target_date).execute()
    
    if not response.data:
        print(f"No comics found for date {target_date}")
        return
    
    print(f"Found {len(response.data)} comics for date {target_date}:")
    for comic in response.data:
        print(f"ID: {comic['id']}, Title: {comic['title']}")
    
    return response.data

if __name__ == "__main__":
    print("Checking database contents...")
    
    # List all comics
    list_comics()
    
    # Uncomment to get a specific comic by ID
    # get_comic_by_id(1)
    
    # Uncomment to get comics for today
    # today = date.today().isoformat()
    # get_comics_by_date(today)