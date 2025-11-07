from flask import Blueprint, render_template, current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Safely get values (avoids KeyError if not found)
    supabase_url = current_app.config.get('SUPABASE_URL')
    supabase_key = current_app.config.get('SUPABASE_KEY')

    return render_template(
        'login.html',
        config={
            'SUPABASE_URL': supabase_url,
            'SUPABASE_KEY': supabase_key
        }
    )

@main.route('/dashboard')
def dashboard():
    return "Dashboard page - to be implemented"
