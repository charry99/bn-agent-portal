"""
Configuration module for Billions Network Agent Portal
Handles environment-based configuration loading
"""

import os
from datetime import timedelta
from pathlib import Path

# Get the root directory of the application
BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base configuration class with default values"""
    
    # ========================================
    # Flask Configuration
    # ========================================
    DEBUG = False
    TESTING = False
    
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # ========================================
    # Database Configuration
    # ========================================
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False
    
    # Use SQLite by default, but allow PostgreSQL via environment variable
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{BASE_DIR / "instance" / "agent_portal.db"}'
    )
    
    # Engine options - only for non-SQLite databases
    if 'sqlite' in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_ENGINE_OPTIONS = {}
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {
            'pool_size': 10,
            'pool_recycle': 3600,
            'pool_pre_ping': True,
        }
    
    # ========================================
    # File Upload Configuration
    # ========================================
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', BASE_DIR / 'uploads')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf'}
    
    # ========================================
    # Session Configuration
    # ========================================
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # ========================================
    # Security Configuration
    # ========================================
    SEND_FILE_MAX_AGE_DEFAULT = 0  # Don't cache static files
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # ========================================
    # CORS Configuration
    # ========================================
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # ========================================
    # Logging Configuration
    # ========================================
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = Path(os.environ.get('LOG_FILE', BASE_DIR / 'logs' / 'agent_portal.log'))
    
    # ========================================
    # Email Configuration (Optional)
    # ========================================
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 25))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'False') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', None)
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', None)
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@billionsnetwork.com')
    
    # ========================================
    # Cache Configuration
    # ========================================
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT = int(os.environ.get('CACHE_DEFAULT_TIMEOUT', 300))
    
    # ========================================
    # Pagination Configuration
    # ========================================
    ITEMS_PER_PAGE = int(os.environ.get('ITEMS_PER_PAGE', 12))
    LEADS_PER_PAGE = int(os.environ.get('LEADS_PER_PAGE', 20))
    
    # ========================================
    # API Configuration
    # ========================================
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT', '100/hour')
    API_TITLE = 'Billions Network Agent Portal API'
    API_VERSION = '1.0.0'
    
    # ========================================
    # Feature Flags
    # ========================================
    ENABLE_REGISTRATION = os.environ.get('ENABLE_REGISTRATION', 'True') == 'True'
    ENABLE_EMAIL_NOTIFICATIONS = os.environ.get('ENABLE_EMAIL_NOTIFICATIONS', 'False') == 'True'
    ENABLE_SMS_NOTIFICATIONS = os.environ.get('ENABLE_SMS_NOTIFICATIONS', 'False') == 'True'
    
    # ========================================
    # Application Information
    # ========================================
    APP_NAME = 'Billions Network Agent Portal'
    APP_VERSION = '1.0.0'
    ORGANIZATION_NAME = 'Billions Network'
    ORGANIZATION_URL = 'https://billionsnetwork.com'    
    # ========================================
    # Agent Information
    # ========================================
    AGENT_INFO = {
        "name": "Nimmakayala Prasad",
        "title": "Billions Network Agent",
        "email": "ajaionline999@gmail.com",
        "city": "Hyderabad, Telangana",
        "bio": "Crypto enthusiast and verified Billions Network Agent. Building trust in the decentralized world with blockchain-backed identity and Web3 technology.",
        "experience": "9+ Years Experience",
        
        # Your Billions Network DID
        "agent_did": "did:iden3:billions:main:2VmAkXrihYaM5GFwgwhz4ytE2ZDd1xmog7c9kDwBvL",
        "network": "billions:main",
    }    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Create necessary directories (but don't fail on read-only filesystems like Vercel)
        try:
            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            os.makedirs(Config.LOG_FILE.parent, exist_ok=True)
            os.makedirs(BASE_DIR / 'instance', exist_ok=True)
        except (OSError, PermissionError):
            # Silently ignore errors on read-only filesystems (Vercel, etc.)
            pass


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = os.environ.get('SQL_ECHO', 'False') == 'True'
    SESSION_COOKIE_SECURE = False
    SEND_FILE_MAX_AGE_DEFAULT = 0  # Don't cache during development
    CACHE_DEFAULT_TIMEOUT = 60  # Shorter cache in development
    
    # Use SQLite for development
    if not os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR / "instance" / "agent_portal.db"}'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year
    CACHE_DEFAULT_TIMEOUT = 3600  # Longer cache in production
    
    # Database must be PostgreSQL in production
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://user:password@localhost/agent_portal'
    )
    
    # Ensure HTTPS
    PREFERRED_URL_SCHEME = 'https'


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    
    # Use in-memory SQLite for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
    # Disable CSRF token checking in tests
    WTF_CSRF_ENABLED = False
    
    # Faster password hashing in tests
    BCRYPT_LOG_ROUNDS = 4
    
    # Disable rate limiting in tests
    RATELIMIT_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    
    return config.get(env, config['default'])
