import mysql.connector
from decouple import Config, RepositoryEnv
config = Config(RepositoryEnv('.env'))

# Connect to your MySQL Server
# change user and password to your username and password respectively
dataBase = mysql.connector.connect( host=config('DB_HOST', default='localhost'), user = config('DB_USER'), passwd = config('DB_PASS'), auth_plugin='mysql_native_password' )

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database, dcrn_db will be the name of your database (you can change this)
cursorObject.execute("CREATE DATABASE CourseU_DB")

print("Database created successfully")


# To run this program, open a terminal window and type:
# python3 mydb.py
# and then it will automatically create the database for you.