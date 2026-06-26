from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    """Returns a new Supabase client instance."""
    url: str = settings.SUPABASE_URL
    key: str = settings.SUPABASE_KEY
    return create_client(url, key)

# Singleton-like client if needed for general admin tasks
supabase_client: Client = get_supabase_client()
