"""Deploys environment preferences based on DJANGO_ENV .env set variable."""
import sys
import os
from dotenv import load_dotenv


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()
_env= os.environ.get('DJANGO_ENV').lower()
print('Deploying environment...')

if _env== 'development':
    from backend.config.settings.development import *
    ALLOWED_HOSTS= ALLOWED_HOSTS
    ROOT_URLCONF= ROOT_URLCONF
    print('Development environment deployed successfully!')
elif _env== 'production':
    from backend.config.settings.production import *
    print('Production environment deployed successfully!')
else:
    raise ValueError(
        f'Unexpected DJANGO_ENV variable!'

    )