from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Command to do Create the Database, Create the Superuser, and load the JSON data, and run the server'

    def add_argument(self, parser):
        pass
        
    def handle(self, *args, **options):
        try:
            # Create the Database by running a python file
            print("Creating the Database")
            exec(open("./create_database.py").read())
            
            # Create the Superuser
            print("Creating the Superuser")
            # exec(open("./create_superuser.py").read())
            call_command('createsuperuser')
            
            # Load the CSV data
            print("Loading the CSV data")
            call_command('load_csv_data')

            # Run the server
            print("Running the server")
            # exec(open("./manage.py runserver").read())
            call_command('runserver')

        except Exception as e:
            CommandError(repr(e))
