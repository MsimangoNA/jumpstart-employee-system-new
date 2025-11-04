import os
from decouple import config # type: ignore

class Config:
    SUPABASE_URL = config('https://hdzdxwssctktnlxsalws.supabase.co')
    SUPABASE_KEY = config('process.env.SUPABASE_KEY')
    SUPABASE_SERVICE_KEY = config('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhkemR4d3NzY3RrdG5seHNhbHdzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTc0MTk4MSwiZXhwIjoyMDc3MzE3OTgxfQ.uperta_ChdHlnNfrHLNdZ83LWpiuStDpxoKnwe0U0ec')
    SECRET_KEY = config('Msimangona@123')