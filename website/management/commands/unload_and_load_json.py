from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Command to do Create the Database, Create the Superuser, and load the JSON data, and run the server'

    def add_argument(self, parser):
        pass
        
    def handle(self, *args, **options):
        try:
            print("Unloading tables to JSON files")
            call_command('save_tables_to_json')

            print("Loading JSON files")
            call_command('load_all_json_to_db --directory ./json_files/')

        except Exception as e:
            CommandError(repr(e))
