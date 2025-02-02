import os
import sys
from dotenv import load_dotenv

load_dotenv()

def main():
    """Main entry point for Django operation. Loads environment variables and sets up application from set configurations."""

    os.environ.get('DJANGO_SETTINGS_MODULE', 'config.deployment')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as import_error:
        raise(
            'Could not import Django. Make sure first it is installed and'
            'available on your PYTHONPATH environment variable.'
            'Or maybe you forgot to activate your virtual environment?'
        ) from import_error

    execute_from_command_line(sys.argv)


if __name__=='__main__':
    main()