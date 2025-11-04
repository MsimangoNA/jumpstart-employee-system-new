from flask import Blueprint, render_template, current_app

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('login.html', 
                         config={
                             'SUPABASE_URL': current_app.config['SUPABASE_URL'],
                             'SUPABASE_KEY': current_app.config['SUPABASE_KEY']
                         })

@main.route('/dashboard')
def dashboard():
    return "Dashboard page - to be implemented"