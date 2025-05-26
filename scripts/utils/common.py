import os
import sys
from typing import Optional
import logging
from datetime import date

# Add the project root to the path so we can import modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment() -> None:
    """Setup the environment for scripts"""
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Check if Supabase credentials are set
    if not os.environ.get("SUPABASE_URL") or not os.environ.get("SUPABASE_KEY"):
        logger.error("Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_KEY in your .env file.")
        sys.exit(1)

def format_comic_output(comic: dict, include_panels: bool = True) -> str:
    """Format comic data for console output"""
    output = [
        f"Comic ID: {comic['id']}",
        f"Title: {comic['title']}",
        f"Date: {comic['date']}"
    ]
    
    if include_panels and 'panels' in comic:
        output.append("Panels:")
        for i, panel in enumerate(comic['panels'], 1):
            output.extend([
                f"  Panel {i}:",
                f"    Sentence: {panel['sentence']}",
                f"    Image URL: {panel['image_url']}"
            ])
    
    return "\n".join(output)

def parse_date(date_str: Optional[str] = None) -> date:
    """Parse date string or return today's date"""
    if not date_str:
        return date.today()
    try:
        year, month, day = map(int, date_str.split('-'))
        return date(year, month, day)
    except ValueError as e:
        logger.error(f"Invalid date format. Please use YYYY-MM-DD. Error: {e}")
        sys.exit(1) 