from core.management.commands.base_db_manage import BaseDBCommand
from config.settings.session_manager import get_db_session
from config.settings.database import Base
from tabulate import tabulate
from sqlalchemy.sql import text

class Command(BaseDBCommand):
    help='Fetch and display database content'

    def handle(self, *args, **options):
        """Fetches all table data and displays it in a formatted way."""
        self.stdout.write(self.style.SUCCESS('Fetching database...'))

        with get_db_session() as session:
            for table in Base.metadata.tables.values():
                self.stdout.write(self.style.WARNING(f'\n Table: {table.name}'))

                try:
                    query=text(f'SELECT * FROM {table.name};')
                    rows= session.execute(query).fetchall()
                    columns= session.execute(query).keys()

                    if rows:
                        self.stdout.write(tabulate(
                            rows,
                            headers=columns,
                            tablefmt='psql'
                        )),
                    else:
                        self.stdout.write(self.style.NOTICE(f'No records found in {table.name}'))

                except Exception as exc:
                    self.stderr.write(self.style.ERROR(f'Error fetching {table.name}: {str(exc)}'))

        self.stdout.write(self.style.SUCCESS('\n Database content fetched successfully!'))