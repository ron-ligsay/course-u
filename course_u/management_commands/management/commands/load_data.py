from django.core.management.base import BaseCommand
import csv
import os
import mysql.connector
#from website.models import Specialization, Field  # Import your models
#from assessment.models import Test, QuestionSet, UserResponse
#from personality.models import  MBTI, MBTISet, MBTIResponse
from django.apps import apps

# from decouple import Config, RepositoryEnv
# config = Config(RepositoryEnv('.env'))

# utilities
from utilities.model_utils import get_all_models, extract_field_types, get_model_table_name, get_csv_table_mapping


class Command(BaseCommand):
    help = 'Import data from CSV files to MySQL database'
    
    def handle(self, *args, **options):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sql2023', # 'sql2023' , 'sawadekap', '022002
            database= 'courseu_db', #config('DB_NAME', default = 'courseu_db')#'courseu_db',
        )

        # check if database exists, if not create it
        cursor = connection.cursor()
        db_name = 'courseu_db'
        
        try:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            self.stdout.write(self.style.SUCCESS("Database created successfully"))
        except:
            print("Exception: Database already exists")
            self.stdout.write(self.style.SUCCESS("Database already exists"))
        

        this_only_list = [
        
        ]
        
        skip_list = [
            'website_userrecommendations', 'website_skill', 
            'assessment_test_skills', 
            'acad_course', 'acad_subject', 'acad_curriculum', 'acad_studentprofile'
            ]
        
        #csv_table_mapping = {}
        csv_table_mapping = get_csv_table_mapping()
        
        
        for csv_file_path, table_info in csv_table_mapping.items():
             # Check if the table exists
            
            query = f"SHOW TABLES LIKE '{table_info['table_name']}'"
            cursor.execute(query)
            table_exists = cursor.fetchone() is not None

            if table_exists:
                print(f"Table '{table_info['table_name']}' already exists. Skipping creating table...")
            else:
                print(f"Creating table '{table_info['table_name']}'...")
                print(table_info['attributes'])
                # ... (create the table)
                col_list = table_info['columns']
                attr_list = table_info['attributes']
                #columnns = ', '.join([f"`{col}` {attr}" for col, attr in zip(table_info['columns'], table_info['attributes'])])
                columns = ', '.join([f"{col} {attr}" for col, attr in zip(col_list, attr_list)])
                print("Columns: ",columns)
                query = f"CREATE TABLE IF NOT EXISTS `{table_info['table_name']}` ( {columns} );"
                print("Query: ",query)
                cursor.execute(query)
                connection.commit()
                print("Now loading data to the table...")
            
            # If table has data, skip loading data
            try:
                query = f"SELECT * FROM {table_info['table_name']}"
                cursor.execute(query)
                table_has_data = cursor.fetchone() is not None
            except:
                table_has_data = False
                print("Exception: Table has no data")

            if table_has_data:
                print(f"Table '{table_info['table_name']}' already has data. Skipping loading data...")
                continue
            else:
                print(f"Loading data to table '{table_info['table_name']}'...")
                # Load data from CSV
                with open(csv_file_path, 'r') as file:
                    csv_reader = csv.DictReader(file)
                    for row in csv_reader:
                        columns = ', '.join(row.keys())
                        placeholders = ', '.join(['%s'] * len(row))
                        query = f"INSERT INTO {table_info['table_name']} ({columns}) VALUES ({placeholders})"
                        print("query: ", query)
                        cursor.execute(query, tuple(row.values()))
                        
        connection.commit()
        cursor.close()
        connection.close()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))


print("Database created successfully")