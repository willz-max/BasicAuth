"""Deploys environment preferences based on DJANGO_ENV .env set variable."""
import sys
import os
from dotenv import load_dotenv
from config.settings.development import ROOT_URLCONF, ALLOWED_HOSTS

load_dotenv()
_env= os.environ.get('DJANGO_ENV').lower()
print('Deploying environment...')

if _env== 'development':
    from config.settings.development import *
    ALLOWED_HOSTS=ALLOWED_HOSTS
    ROOT_URLCONF= ROOT_URLCONF
    print('Development environment deployed successfully!')

elif _env== 'production':
    import config.settings.production as prod
    print('Production environment deployed successfully!')

else:
    raise ValueError(
        f'Unexpected DJANGO_ENV variable!'

    )