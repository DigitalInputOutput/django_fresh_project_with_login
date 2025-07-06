from django.core.management.base import BaseCommand
from django.core.management import call_command
from system.settings import DATABASES, BASE_DIR
import os, glob, getpass, sys
import pymysql

class Command(BaseCommand):
    help = 'Destroy, recreate and reinitialize the database (for development only).'

    def add_arguments(self, parser):
        parser.add_argument('--danger', action='store_true', help='Confirm dangerous reset')
        parser.add_argument('--with-db', action='store_true', help='Also drop and recreate the database (requires root access)')

    def handle(self, *args, **options):
        if not options['danger']:
            self.stdout.write(self.style.ERROR("❌ Use --danger to confirm this destructive operation."))
            sys.exit(1)

        if options['with_db']:
            self.reset_database()

        self.delete_migration_files()
        self.rebuild_migrations()

    def reset_database(self):
        db = DATABASES['default']
        db_name = db['NAME']
        db_user = db['USER']
        db_pass = db['PASSWORD']
        db_host = db['HOST']

        password = getpass.getpass("Enter MySQL root password (for dropping DB): ")
        try:
            connection = pymysql.connect(
                host=db_host,
                user='root',
                password=password
            )
            with connection.cursor() as cursor:
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
                cursor.execute(f"DROP DATABASE IF EXISTS `{db_name}`;")
                self.stdout.write(f"✅ Dropped database {db_name}")
                cursor.execute(f"CREATE DATABASE `{db_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
                cursor.execute(f"CREATE USER IF NOT EXISTS '{db_user}'@'{db_host}' IDENTIFIED BY '{db_pass}';")
                cursor.execute(f"GRANT ALL ON `{db_name}`.* TO '{db_user}'@'{db_host}';")
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            connection.commit()
        finally:
            connection.close()

        self.stdout.write(self.style.SUCCESS("✅ Database reset complete."))

    def delete_migration_files(self):
        project_root = BASE_DIR.parent / 'server'
        for app in os.listdir(project_root):
            migrations_dir = project_root / app / 'migrations'
            if migrations_dir.exists():
                for file in glob.glob(str(migrations_dir / '*.py')):
                    if not file.endswith('__init__.py'):
                        os.remove(file)
                        self.stdout.write(f"🗑 Deleted {file}")

    def rebuild_migrations(self):
        self.stdout.write("📦 Rebuilding migrations...")
        call_command("makemigrations")
        call_command("migrate", interactive=False)
        self.stdout.write(self.style.SUCCESS("✅ Migrations rebuilt."))