"""Deploys environment preferences based on DJANGO_ENV .env set variable."""

import os
from dotenv import load_dotenv

load_dotenv()
_env= os.environ.get('DJANGO_ENV').lower()
print('Deploying environment...')

if _env== 'development':
    from backend.config.settings.development import *
    print('Development environment deployed successfully!')
elif _env== 'production':
    from backend.config.settings.production import *
    print('Production environment deployed successfully!')
else:
    raise ValueError(
        f'Unexpected DJANGO_ENV variable!'

    )