from config.settings.database import Base
from config.settings.session_manager import get_db_session
from core.management.commands.base_db_manage import BaseDBCommand, engine


class Command(BaseDBCommand):
    help='Resets database'

    def handle(self, *args, **options):
        with get_db_session() as session:
            try:
                self.reset_database()
            except Exception as exc:
                self.stdout.write(self.style.NOTICE('Invalid input!'))

    def reset_database(self):
        """Drop and recreate all tables."""
        self.stdout.write(self.style.WARNING('Resetting database...'))
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.stdout.write(self.style.SUCCESS('Database reset and recreated successfully!'))