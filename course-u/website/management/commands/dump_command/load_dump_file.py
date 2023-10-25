
from django.core.management.base import BaseCommand
from django.db import connection
import os

class Command(BaseCommand):
    help = 'Load data from SQL dump file into the database'

    def handle(self, *args, **kwargs):
        # Define the path to your SQL dump file
        sql_dump_file = os.getcwd() + '\dump_file.sql'
        # Read the SQL from the file
        with open(sql_dump_file, 'r') as f:
            sql_statements = f.read()

        # Execute the SQL statements
        with connection.cursor() as cursor:
            cursor.execute(sql_statements)

        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
