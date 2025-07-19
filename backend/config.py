"""
Configuration classes for HomelabWiki application.
Supports different deployment environments with secure environment variable management.
"""

import os
from datetime import timedelta

class Config:
    """Base configuration class with default settings."""
    
    # Flask Core Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    FLASK_ENV = os.environ.get('FLASK_ENV') or 'development'
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///homelab_wiki.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # LDAP/Active Directory Configuration
    LDAP_SERVER = os.environ.get('LDAP_SERVER') or 'your-domain-controller'
    LDAP_PORT = int(os.environ.get('LDAP_PORT') or '389')
    LDAP_USE_SSL = os.environ.get('LDAP_USE_SSL', 'false').lower() == 'true'
    LDAP_USE_TLS = os.environ.get('LDAP_USE_TLS', 'true').lower() == 'true'
    
    # LDAP Bind Configuration
    LDAP_BASE_DN = os.environ.get('LDAP_BASE_DN') or 'DC=yourdomain,DC=local'
    LDAP_BIND_DN = os.environ.get('LDAP_BIND_DN') or 'CN=wikisvc,CN=Users,DC=yourdomain,DC=local'
    LDAP_BIND_PASSWORD = os.environ.get('LDAP_BIND_PASSWORD') or 'your-service-password'
    
    # LDAP Search Configuration
    LDAP_USER_SEARCH_BASE = os.environ.get('LDAP_USER_SEARCH_BASE') or 'CN=Users,DC=yourdomain,DC=local'
    LDAP_GROUP_SEARCH_BASE = os.environ.get('LDAP_GROUP_SEARCH_BASE') or 'CN=Groups,DC=yourdomain,DC=local'
    LDAP_USER_OBJECT_CLASS = os.environ.get('LDAP_USER_OBJECT_CLASS') or 'user'
    LDAP_GROUP_OBJECT_CLASS = os.environ.get('LDAP_GROUP_OBJECT_CLASS') or 'group'
    
    # LDAP Attribute Mapping
    LDAP_USERNAME_ATTRIBUTE = os.environ.get('LDAP_USERNAME_ATTRIBUTE') or 'sAMAccountName'
    LDAP_EMAIL_ATTRIBUTE = os.environ.get('LDAP_EMAIL_ATTRIBUTE') or 'mail'
    LDAP_FIRSTNAME_ATTRIBUTE = os.environ.get('LDAP_FIRSTNAME_ATTRIBUTE') or 'givenName'
    LDAP_LASTNAME_ATTRIBUTE = os.environ.get('LDAP_LASTNAME_ATTRIBUTE') or 'sn'
    LDAP_GROUP_MEMBER_ATTRIBUTE = os.environ.get('LDAP_GROUP_MEMBER_ATTRIBUTE') or 'member'
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or '/app/uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH') or str(16 * 1024 * 1024))  # 16MB default
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx', 'zip', 'tar', 'gz', 'md'}
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    # Security Configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # Application Configuration
    WIKI_TITLE = os.environ.get('WIKI_TITLE') or 'HomelabWiki'
    WIKI_DESCRIPTION = os.environ.get('WIKI_DESCRIPTION') or 'Knowledge Base for Homelab Environment'
    PAGINATION_PER_PAGE = int(os.environ.get('PAGINATION_PER_PAGE') or '20')
    
    # Search Configuration
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    ENABLE_FULL_TEXT_SEARCH = os.environ.get('ENABLE_FULL_TEXT_SEARCH', 'true').lower() == 'true'
    
    # Backup Configuration
    BACKUP_FOLDER = os.environ.get('BACKUP_FOLDER') or '/app/backups'
    AUTO_BACKUP_ENABLED = os.environ.get('AUTO_BACKUP_ENABLED', 'true').lower() == 'true'
    BACKUP_RETENTION_DAYS = int(os.environ.get('BACKUP_RETENTION_DAYS') or '30')

class DevelopmentConfig(Config):
    """Development configuration with debug enabled."""
    
    DEBUG = True
    FLASK_ENV = 'development'
    
    # Less restrictive LDAP settings for development
    LDAP_USE_TLS = False
    LDAP_USE_SSL = False
    
    # Development database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///dev_homelab_wiki.db'
    
    # Development file paths
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or './uploads'
    BACKUP_FOLDER = os.environ.get('BACKUP_FOLDER') or './backups'

class ProductionConfig(Config):
    """Production configuration with security hardening."""
    
    DEBUG = False
    FLASK_ENV = 'production'
    
    # Force HTTPS in production
    PREFERRED_URL_SCHEME = 'https'
    
    # Secure session configuration
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Force environment variables for sensitive data
    SECRET_KEY = os.environ.get('SECRET_KEY')
    LDAP_BIND_PASSWORD = os.environ.get('LDAP_BIND_PASSWORD')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set in production")
    
    # More graceful handling of LDAP_BIND_PASSWORD - warn but don't fail
    if not LDAP_BIND_PASSWORD:
        import warnings
        warnings.warn(
            "LDAP_BIND_PASSWORD environment variable is not set. "
            "LDAP authentication will not work properly.",
            UserWarning
        )

class TestingConfig(Config):
    """Testing configuration with test database."""
    
    TESTING = True
    DEBUG = True
    FLASK_ENV = 'testing'
    
    # Use in-memory database for testing
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False
    
    # Disable LDAP for testing
    LDAP_SERVER = 'localhost'
    LDAP_PORT = 389
    LDAP_USE_SSL = False
    LDAP_USE_TLS = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Return the appropriate configuration based on environment."""
    return config[os.environ.get('FLASK_ENV', 'default')]