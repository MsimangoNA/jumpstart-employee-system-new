import os
from decouple import config

class Config:
    SUPABASE_URL = config('https://hdzdxwssctktnlxsalws.supabase.co')
    SUPABASE_KEY = config('Msimangona@123')
    SUPABASE_SERVICE_KEY = config('5iTH1Wna56EhgGwYTodXDKi8e6phZ46MFvPy/S+KvnyF2WwILei8KCqaRbPS1yuYtRLUJETUrCLz/SSrz+l3Yg==')
    SECRET_KEY = config('FLASK_SECRET_KEY')