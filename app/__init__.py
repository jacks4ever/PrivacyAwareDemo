import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

# Initialize SQLAlchemy
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Enable CORS for all routes and origins
    CORS(app, supports_credentials=True)
    
    # Configure the app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-for-demo-only')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///privacy_demo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEMO_MODE'] = os.environ.get('DEMO_MODE', 'false').lower() == 'true'
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.admin import admin_bp
    from app.routes.scraper import scraper_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(scraper_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Import and initialize demo data if in demo mode
        if app.config['DEMO_MODE']:
            from app.models.demo_data import initialize_demo_data
            initialize_demo_data()
    
    return app