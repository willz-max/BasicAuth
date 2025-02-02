"""Deploys environment preferences based on DJANGO_ENV .env set variable."""
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

load_dotenv()
_env= os.environ.get('DJANGO_ENV').lower()
print('Deploying environment...')

if _env== 'development':
    import settings.development as dev
    ALLOWED_HOSTS=[]
    if not ALLOWED_HOSTS:
        ALLOWED_HOSTS= ['localhost', '127.0.0.1']
        print('Development environment deployed successfully!')
elif _env== 'production':
    import settings.production as prod
    print('Production environment deployed successfully!')
else:
    raise ValueError(
        f'Unexpected DJANGO_ENV variable!'

    )