"""this will contain the environment settings
flask needs them before starting"""
import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET') or 'fdisfhsofjsoifsdfhds'
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database. Used during testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://collinsnjau:wrestlemania34@localhost/test_db'
    DEBUG = True

class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
}