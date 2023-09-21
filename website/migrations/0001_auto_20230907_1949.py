# Generated by Django 4.2.4 on 2023-09-07 11:29

from django.db import migrations
import os

def create_database_and_load_sql(apps, schema_editor):
    # Create the database
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute('CREATE DATABASE IF NOT EXISTS courseu_db;')

    # Define the path to your SQL file
    sql_file = os.getcwd() + '\dump_file.sql'

    # Read the SQL from the file
    with open(sql_file, 'r') as f:
        sql_statements = f.read()

    # Execute the SQL statements
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(sql_statements)


class Migration(migrations.Migration):

    dependencies = [
        
    ]

    operations = [
    ]