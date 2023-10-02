from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Delete all database tables'

    def handle(self, *args, **options):
        # Get a list of table names from the database
        table_names1 = connection.introspection.table_names()
        print(table_names1)
        table_names = [
            'assessment_test', 'assessment_questionset', 'assessment_userresponse', 'website_specialization', 'website_userprofile', 'jobs_jobposting'
        ]

        # Iterate through the table names and delete each table
        with connection.cursor() as cursor:
            for table_name in table_names:
                cursor.execute(f"DROP TABLE {table_name};")
                self.stdout.write(self.style.SUCCESS(f'Deleted table: {table_name}'))

        self.stdout.write(self.style.SUCCESS('All database tables deleted'))
