"""
HomelabWiki Flask Application Factory.
Creates and configures the Flask application with all necessary extensions.
"""

import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_session import Session
from flask_wtf.csrf import CSRFProtect

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_name=None):
    """
    Application factory function that creates and configures Flask app.
    
    Args:
        config_name (str): Configuration name ('development', 'production', 'testing')
        
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    # Configure CORS
    CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'], 
         supports_credentials=True)
    
    # Configure session
    Session(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Configure logging
    configure_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint for monitoring."""
        return {'status': 'healthy', 'service': 'HomelabWiki'}, 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Create upload and backup directories
    create_directories(app)
    
    return app

def configure_logging(app):
    """Configure application logging."""
    if not app.debug and not app.testing:
        # Configure logging for production
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(name)s %(message)s',
            handlers=[
                logging.FileHandler('logs/homelab_wiki.log'),
                logging.StreamHandler()
            ]
        )
        app.logger.setLevel(logging.INFO)
        app.logger.info('HomelabWiki startup')
    else:
        # Configure logging for development
        logging.basicConfig(level=logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)

def register_blueprints(app):
    """Register application blueprints."""
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

def register_error_handlers(app):
    """Register error handlers for the application."""
    
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        return {'error': 'Access forbidden'}, 403
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        return {'error': 'Authentication required'}, 401

def create_directories(app):
    """Create necessary directories for file storage."""
    directories = [
        app.config['UPLOAD_FOLDER'],
        app.config['BACKUP_FOLDER'],
        'logs'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            app.logger.info(f'Created directory: {directory}')

# Import models to ensure they are registered with SQLAlchemy
from app.models import user, page, file