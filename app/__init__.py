from flask import Flask
from config import Config
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Register blueprints
    from app.routes import main
    from app.auth import auth_bp
    
    app.register_blueprint(main)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app