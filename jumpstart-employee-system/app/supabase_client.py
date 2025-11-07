import os
from supabase import create_client, Client
from config import Config

class SupabaseClient:
    _instance = None
    
    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            cls._instance = create_client(
                Config.SUPABASE_URL,
                Config.SUPABASE_KEY
            )
        return cls._instance
    
    @classmethod
    def get_admin_client(cls) -> Client:
        return create_client(
            Config.SUPABASE_URL,
            Config.SUPABASE_SERVICE_KEY
        )

def get_supabase():
    return SupabaseClient.get_client()

def get_supabase_admin():
    return SupabaseClient.get_admin_client()