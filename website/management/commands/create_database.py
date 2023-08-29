import mysql.connector

# Connect to your MySQL Server
# change user and password to your username and password respectively
dataBase = mysql.connector.connect( host="localhost", user = "root", passwd = "022002", auth_plugin='mysql_native_password' )

# prepare a cursor object
cursorObject = dataBase.cursor()

# Create a database, dcrn_db will be the name of your database (you can change this)
cursorObject.execute("CREATE DATABASE CourseU_DB")

print("Database created successfully")


# To run this program, open a terminal window and type:
# python3 mydb.py
# and then it will automatically create the database for you.