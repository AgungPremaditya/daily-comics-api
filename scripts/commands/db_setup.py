import logging
from typing import List, Dict, Any
from db import get_supabase_client
from ..utils.common import setup_environment

logger = logging.getLogger(__name__)

def get_table_definitions() -> List[Dict[str, Any]]:
    """Get the definitions for all required tables"""
    return [
        {
            "name": "comics",
            "columns": [
                {"name": "id", "type": "integer", "primary": True},
                {"name": "title", "type": "text", "required": True},
                {"name": "date", "type": "date", "required": True},
                {"name": "story_id", "type": "integer", "required": True},
            ]
        },
        {
            "name": "panels",
            "columns": [
                {"name": "id", "type": "integer", "primary": True},
                {"name": "comic_id", "type": "integer", "required": True},
                {"name": "sentence", "type": "text", "required": True},
                {"name": "image_url", "type": "text", "required": True},
                {"name": "panel_order", "type": "integer", "required": True},
            ],
            "foreign_keys": [
                {"column": "comic_id", "references": "comics(id)"}
            ]
        }
    ]

def check_table_exists(table_name: str) -> bool:
    """Check if a table exists in the database"""
    try:
        supabase = get_supabase_client()
        supabase.table(table_name).select("count", count="exact").execute()
        logger.info(f"Table '{table_name}' already exists.")
        return True
    except Exception:
        logger.info(f"Table '{table_name}' does not exist.")
        return False

def print_table_creation_instructions(table_def: Dict[str, Any]) -> None:
    """Print instructions for creating a table"""
    logger.info(f"\nPlease create the '{table_def['name']}' table in your Supabase dashboard with the following columns:")
    
    for col in table_def['columns']:
        required = "NOT NULL" if col.get('required', False) else "NULL"
        primary = "PRIMARY KEY" if col.get('primary', False) else ""
        logger.info(f"- {col['name']}: {col['type']} {required} {primary}".strip())
    
    if 'foreign_keys' in table_def:
        logger.info("\nForeign Keys:")
        for fk in table_def['foreign_keys']:
            logger.info(f"- {fk['column']} REFERENCES {fk['references']}")

async def setup_database() -> None:
    """Set up the Supabase database with required tables"""
    try:
        # Setup environment first
        setup_environment()
        
        # Get table definitions
        tables = get_table_definitions()
        
        # Check each table
        for table_def in tables:
            if not check_table_exists(table_def['name']):
                print_table_creation_instructions(table_def)
        
        logger.info("\nDatabase setup check completed.")
        
    except Exception as e:
        logger.error(f"Error setting up database: {e}")
        raise 