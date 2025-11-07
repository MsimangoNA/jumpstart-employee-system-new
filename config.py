from decouple import config

class Config:
    SECRET_KEY = config('FLASK_SECRET_KEY')
    SUPABASE_URL = config('SUPABASE_URL')
    SUPABASE_KEY = config('SUPABASE_KEY')
    SUPABASE_SERVICE_KEY = config('SUPABASE_SERVICE_KEY')
