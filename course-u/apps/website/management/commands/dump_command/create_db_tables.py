# Import necessary modules
from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps
from django.db import connection


class Command(BaseCommand):
    help = 'Create database tables based on Django models'

    def handle(self, *args, **options):
        # Iterate through installed apps
        for app_config in apps.get_app_configs():
            # Iterate through models in each app
            for model in app_config.get_models():
                self.stdout.write(self.style.SUCCESS('Model: {model}'))
                # Get model's database table name
                table_name = model._meta.db_table
                self.stdout.write(self.style.SUCCESS('Model: {table_name}'))
                # Get model's fields
                fields = model._meta.fields
                # Generate SQL statement
                columns = ', '.join([f"{field.column} {field.db_type(connection=connection)}" for field in fields])
                query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});"
                # Execute SQL statement
                with connection.cursor() as cursor:
                    cursor.execute(query)
        
        self.stdout.write(self.style.SUCCESS('Database tables created successfully'))
