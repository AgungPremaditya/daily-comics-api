import os
import sys
from dotenv import load_dotenv

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.supabase_client import get_supabase_client

def setup_supabase():
    """
    Set up the Supabase database with the required tables.
    
    Note: This script assumes you have already created a project in Supabase
    and have the necessary permissions to create tables.
    """
    try:
        # Get the Supabase client
        supabase = get_supabase_client()
        
        # Check if the comics table exists by trying to select from it
        try:
            supabase.table("comics").select("count", count="exact").execute()
            print("Comics table already exists.")
        except Exception:
            # Create the comics table if it doesn't exist
            # Note: In Supabase, you typically create tables through the web interface
            # or using SQL migrations. This is just a placeholder to show how you might
            # interact with Supabase programmatically.
            print("Please create the 'comics' table in your Supabase dashboard with the following columns:")
            print("- id: integer (primary key)")
            print("- title: text")
            print("- author: text")
            print("- published_date: date")
            print("- image_url: text (optional)")
            print("- description: text (optional)")
            
        # Insert some sample data if the table is empty
        response = supabase.table("comics").select("count", count="exact").execute()
        if response.count == 0:
            sample_comics = [
                {
                    "title": "Garfield",
                    "author": "Jim Davis",
                    "published_date": "2023-01-01",
                    "image_url": "https://example.com/garfield.jpg",
                    "description": "A comic about a lazy cat who loves lasagna."
                },
                {
                    "title": "Calvin and Hobbes",
                    "author": "Bill Watterson",
                    "published_date": "2023-01-02",
                    "image_url": "https://example.com/calvin.jpg",
                    "description": "A comic about a boy and his imaginary tiger friend."
                }
            ]
            supabase.table("comics").insert(sample_comics).execute()
            print("Sample comics inserted successfully.")
        else:
            print(f"Comics table already has {response.count} records.")
            
        print("Supabase setup completed successfully.")
        
    except Exception as e:
        print(f"Error setting up Supabase: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Check if Supabase credentials are set
    if not os.environ.get("SUPABASE_URL") or not os.environ.get("SUPABASE_KEY"):
        print("Error: Supabase credentials not found. Please set SUPABASE_URL and SUPABASE_KEY in your .env file.")
        sys.exit(1)
    
    # Run the setup
    setup_supabase()