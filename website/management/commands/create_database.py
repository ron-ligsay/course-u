from django.core.management.base import BaseCommand, CommandError
import mysql.connector
from decouple import Config, RepositoryEnv
config = Config(RepositoryEnv('.env'))

# Connect to your MySQL Server
# change user and password to your username and password respectively
dataBase = mysql.connector.connect( host=config('DB_HOST', default='localhost'), user = config('DB_USER'), passwd = config('DB_PASS'), auth_plugin='mysql_native_password' )


class Command(BaseCommand):
    help = 'Create the database'

    def handle(self, *args, **kwargs):
        with dataBase.cursor() as cursor:
            # Create a database, dcrn_db will be the name of your database (you can change this)
            cursor.execute("CREATE DATABASE CourseU_DB")
        self.stdout.write(self.style.SUCCESS("Database created successfully"))

  

# To run this program, open a terminal window and type:
# python3 mydb.py
# and then it will automatically create the database for you.