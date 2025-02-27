import logging
from django.core.management.base import BaseCommand
from config.settings.database import Base, get_engine
from config.settings.session_manager import get_db_session

engine= get_engine()

class BaseDBCommand(BaseCommand):
    """Base class for database-related management commands."""

    def reset_database(self):
        """Drop and recreate all tables."""
        self.stdout.write('Resetting database...')
        Base.metadata.drop_alll(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.stdout.write(self.style.SUCCESS('Database reset and recreated successfully!'))

    def seed_database(self):
        """Seed database with generic test data. Override in subclass if necessary."""
        self.stdout.write(self.style.WARNING('No seeding logic defined.'))

    def migrate_database(self):
        """Run migrations (optional if using Alembic)."""
        self.stdout.write('Applying migrations...')
        # If using Alembic:
        # import subprocess
        # subprocess.run(['alembic', 'upgrade', 'head'])
        self.stdout.write(self.style.SUCCESS('Migrations applied successfully!'))