#!/usr/bin/env python3
import asyncio
import argparse
import logging
from commands.db_setup import setup_database
from utils.common import setup_environment

logger = logging.getLogger(__name__)

def setup_parser() -> argparse.ArgumentParser:
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(description="Setup Supabase database")
    parser.add_argument("--check-only", action="store_true", help="Only check table existence without creating")
    return parser

async def main() -> None:
    """Main entry point"""
    # Setup environment
    setup_environment()
    
    # Parse arguments
    parser = setup_parser()
    args = parser.parse_args()
    
    try:
        await setup_database()
    except Exception as e:
        logger.error(f"Error setting up database: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())