from core.management.commands.base_db_manage import BaseDBCommand
from config.settings.session_manager import get_db_session
from modules.auth.auth_models import ClientUser


class Command(BaseDBCommand):
    help= 'Manage authentication-related database operations (reset, seed, migrate)'

    def add_arguments(self, parser):
        parser.add_argument(
            'action',
            type=str,
            choices=[
                'reset',
                'seed',
                'migrate',
            ],
            help='Choose an action: reset, seed, migrate'
        )

    def handle(self, *args, **options):
        action= options['action']
        if action=='reset':
            self.reset_database()
        elif action=='seed':
            self.seed_database()
        elif action=='migrate':
            self.migrate_database()
        else:
            self.stdout.write(self.style.ERROR('Invalid action'))

    def seed_database(self):
        """Seed authentication-related test users."""
        self.stdout.write('Seeding authentication database...')
        with get_db_session() as session:
            user1= ClientUser(
                first_name='John',
                last_name='Doe',
                email='johndoe@gmail.com',
                password_hash='hashed_pwd',
            )
            user2= ClientUser(
                first_name='Jane',
                last_name='Dae',
                email='janedae@gmail.com',
                password_hash='hashed_pwd',
            )
            session.add_all([user1, user2])

        self.stdout.write(self.style.SUCCESS('Authentication database seeded successfully!'))