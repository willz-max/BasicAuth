import os
from functools import lru_cache
from typing import List
from dotenv import load_dotenv
from backend.config.settings.base import BaseConfig

load_dotenv()


class DevelopmentConfig(BaseConfig):
    """Development environment specific configurations."""
    def __init__(self):
        super().__init__()

        self._debug= True
        self._allowed_hosts= os.environ.get('DJANGO_ALLOWED_HOSTS').split(',')
        self._cors_allow_all_origins= True
        self._root_urlconf= 'backend.config.urls'

    @property
    def debug(self)-> bool:
        """Debug configuration. Set to True in development environments only."""
        return self._debug

    @property
    def allowed_hosts(self)-> List[str]:
        """Defined list of allowed hosts."""
        return self._allowed_hosts

    @property
    def cors_allow_all_origins(self)-> bool:
        """Temporary disabling of CORS to accept from all origins."""
        return self._cors_allow_all_origins

    @property
    def root_urlconf(self)-> str:
        """Project root URL."""
        return self._root_urlconf


@lru_cache()
def get_dev_config()-> DevelopmentConfig:
    """Cached instance of DevelopmentConfig."""
    return DevelopmentConfig()


config= get_dev_config()


# ==========
# EXPORTS
# ==========

#SECRET_KEY= config.secret_key
#DATABASES= config.databases

DEBUG= config.debug
ALLOWED_HOSTS= config.allowed_hosts
CORS_ALLOW_ALL_ORIGINS= config.cors_allow_all_origins
ROOT_URLCONF= config.root_urlconf