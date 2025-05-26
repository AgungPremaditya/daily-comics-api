#!/usr/bin/env python3
import asyncio
import argparse
import logging
from commands.db_check import (
    list_comics,
    get_comic_by_id,
    get_comics_by_date,
    insert_test_comic
)
from utils.common import setup_environment

logger = logging.getLogger(__name__)

def setup_parser() -> argparse.ArgumentParser:
    """Setup command line argument parser"""
    parser = argparse.ArgumentParser(description="Check and manage database contents")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # List comics command
    subparsers.add_parser("list", help="List all comics")
    
    # Get comic by ID command
    get_parser = subparsers.add_parser("get", help="Get a specific comic by ID")
    get_parser.add_argument("id", type=int, help="Comic ID")
    
    # Get comics by date command
    date_parser = subparsers.add_parser("date", help="Get comics for a specific date")
    date_parser.add_argument("--date", type=str, help="Date in YYYY-MM-DD format (default: today)")
    
    # Insert test comic command
    subparsers.add_parser("test", help="Insert a test comic")
    
    return parser

async def main() -> None:
    """Main entry point"""
    # Setup environment
    setup_environment()
    
    # Parse arguments
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    try:
        if args.command == "list":
            await list_comics()
        elif args.command == "get":
            await get_comic_by_id(args.id)
        elif args.command == "date":
            await get_comics_by_date(args.date)
        elif args.command == "test":
            await insert_test_comic()
    except Exception as e:
        logger.error(f"Error executing command: {e}")

if __name__ == "__main__":
    asyncio.run(main())