import os
import sys
import subprocess
import importlib
from django.core.management.base import BaseCommand
from django.conf import settings


def ensure_mysql_connector():
    """Ensure mysql-connector-python is installed, install if missing."""
    try:
        importlib.import_module("mysql.connector")
    except ImportError:
        print("mysql-connector-python not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mysql-connector-python"])
    finally:
        global mysql
        import mysql.connector as mysql


class Command(BaseCommand):
    help = "Run pre-migrate SQL (raw), then migrate in a new process, then post-migrate SQL."

    def run_sql_file_raw(self, path, db_name=None):
        """Run SQL file without using Django's connection."""
        if not os.path.exists(path):
            self.stdout.write(self.style.WARNING(f"SQL file not found: {path}"))
            return

        db_settings = settings.DATABASES["default"]

        self.stdout.write(f"==> Running {path} (raw connection)")
        conn = mysql.connect(
            host=db_settings["HOST"] or "127.0.0.1",
            port=int(db_settings.get("PORT") or 3306),
            user=db_settings["USER"],
            password=db_settings["PASSWORD"],
            database=db_name or None
        )
        cursor = conn.cursor()
        with open(path, "r", encoding="utf-8") as f:
            sql_content = f.read()
        for stmt in [s.strip() for s in sql_content.split(";") if s.strip()]:
            cursor.execute(stmt)
        conn.commit()
        cursor.close()
        conn.close()

    def run_sql_file_django(self, path):
        """Run SQL file using Django's default DB connection."""
        if not os.path.exists(path):
            self.stdout.write(self.style.WARNING(f"SQL file not found: {path}"))
            return

        # Import here so connection happens after migrate
        from django.db import connection

        self.stdout.write(f"==> Running {path} (Django connection)")
        with open(path, "r", encoding="utf-8") as f:
            sql_content = f.read()
        with connection.cursor() as cursor:
            for stmt in [s.strip() for s in sql_content.split(";") if s.strip()]:
                cursor.execute(stmt)

    def handle(self, *args, **options):
        ensure_mysql_connector()

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        SQL_DIR = os.path.join(BASE_DIR, "sql")
        pre_file = os.path.join(SQL_DIR, "pre_migrate.sql")
        post_file = os.path.join(SQL_DIR, "post_migrate.sql")

        # Step 1: Run pre-migrate SQL without Django
        self.run_sql_file_raw(pre_file, db_name=None)

        # Step 2: Run Django migrations in a new process (so DB exists)
        self.stdout.write("==> Running Django migrations")
        subprocess.check_call([sys.executable, "manage.py", "migrate"])

        # Step 3: Run post-migrate SQL using Django's connection
        self.run_sql_file_django(post_file)

        self.stdout.write(self.style.SUCCESS("Database initialized successfully."))
