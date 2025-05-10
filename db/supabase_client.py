import os
from dotenv import load_dotenv
from supabase import create_client, Client  # This should be from supabase directly

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")

if not supabase_url or not supabase_key:
    raise ValueError("Missing Supabase credentials. Please check your .env file.")

supabase: Client = create_client(supabase_url, supabase_key)

def get_supabase_client() -> Client:
    """Returns the Supabase client instance."""
    return supabase