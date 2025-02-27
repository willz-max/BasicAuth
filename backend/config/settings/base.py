"""Base configurations for Django application and extension point for development and production environments."""

import os
from pathlib import Path
from typing import List, Dict, Any
from functools import lru_cache
from dotenv import load_dotenv
from .database import postgresql_config
#from config.settings.cache import redis_cache_config
#from config.settings.session import redis_session_config


load_dotenv()

class BaseConfig:
    """Core configurations handling Django."""
    def __init__(self):
        self._secret_key= os.environ.get('DJANGO_SECRET_KEY')
        self.base_dir= Path(__file__).resolve().parent.parent.parent
        self._db_config= postgresql_config().django_db_config
        self._validate_environ()

    @staticmethod
    def _validate_environ()->None:
        """Validates required environments variables if existing."""
        required=[
            'DJANGO_SECRET_KEY',
            'DB_NAME',
            'DB_USER',
            'DB_PASSWORD',
            'DB_HOST',
            'DB_PORT',
        ]
        missing_var=[var for var in required if not os.environ.get(var)]
        if missing_var:
            raise ValueError(
                f'Missing required environment variable: {', '.join(missing_var)}'
            )

    @property
    def secret_key(self)-> str:
        """Secure secret key fetcher with validation."""
        if not self._secret_key:
            raise ValueError(
                f'SECRET_KEY environment expected but not defined.'
            )
        return self._secret_key

    @property
    def installed_apps(self)-> List[str]:
        """List of installed apps defining third party and project specific applications."""
        third_party=[
            #'corsheaders',
            #'django_redis',
            #'celery',
        ]
        project_apps=[
            'core',
        ] # custom applications here
        return third_party+ project_apps

    @property
    def databases(self)-> Dict[str, Dict[str, Any]]:
        """Database configurations."""
        return self._db_config

    @property
    def middleware(self)-> List[str]:
        """List of deployed middleware. CAUTION: Order of arrangement is critical!"""
        default=[
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
        ]
        custom=[] # custom middleware here
        return default + custom


@lru_cache()
def base_config()-> BaseConfig:
    """Cached instance of BaseConfig for faster operations."""
    return BaseConfig()


config= base_config()


# ==========
# EXPORTS
# ==========

SECRET_KEY= config.secret_key
BASE_DIR= config.base_dir
DATABASES= config.databases
MIDDLEWARE= config.middleware
INSTALLED_APPS= config.installed_apps

ASGI_APPLICATION= 'config.asgi.application'
WSGI_APPLICATION= 'config.wsgi.application'

CSRF_TRUSTED_ORIGINS=[]

# Other
LANGUAGE_CODE= 'en-us'
TIME_ZONE= 'UTC'
USE_L10N= True
USE_I10N= True
USE_TZ= True
