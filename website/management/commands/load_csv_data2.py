from django.core.management.base import BaseCommand
import csv
import os
import mysql.connector
from website.models import Specialization, Field  # Import your models
from assessment.models import Test, QuestionSet, UserResponse
from django.apps import apps

from decouple import Config, RepositoryEnv
config = Config(RepositoryEnv('.env'))

class Command(BaseCommand):
    help = 'Import data from CSV files to MySQL database'
    
    def handle(self, *args, **options):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sql2023',
            database= config('DB_NAME', default = 'courseu_db2')#'courseu_db',
        )

        base_dir = os.getcwd()
        csv_table_mapping = {
            base_dir + '\\static\\csv\\specialization1.csv': {
                'table_name': 'website_specialization',
                'model_name': 'Specialization',
                'columns': ['specialization_id', 'field_id', 'title','description','roadmap_id',],
                'attributes': ['INT PRIMARY KEY', 'INT', 'VARCHAR(100)', 'VARCHAR(1000)', 'INT',]
            },
            base_dir + '\\static\\csv\\field.csv': {
                'table_name': 'website_field',
                'model_name' : 'Field',
                'columns' : ['field','field_name','description'],
                'attributes' : ['INT PRIMAMRY KEY', 'VARCHAR(150)', 'VARCHAR(1000)']
            },
            base_dir + '\\src\\job_post_scrapy\\jobs\\jobs_clean.csv': {
                'table_name': 'jobs_jobposting',
                'model_name': 'JobPosting',
                #link,keyword,title,company,company_link,date,link_clean,id
                'columns': ['keyword','title','company','company_link','date','link_clean','id'],
                'attributes': ['VARCHAR(100)', 'VARCHAR(100)', 'VARCHAR(100)', 'VARCHAR(6000)', 'VARCHAR(100)', 'VARCHAR(4000)', 'INT PRIMARY KEY']
            },
            base_dir + '\\static\\csv\\test_2.csv': {
                'table_name': 'assessment_test',
                'model_name': 'Test',
                'columns':  ['question_id', 'topic','question','description','options', 'correct_option',],
                'attributes': ['INT PRIMARY KEY', 'VARCHAR(1000)', 'VARCHAR(1000)', 'VARCHAR(1000)', 'JSON', 'INT',]
            },
            base_dir + '\\static\\csv\\questionset.csv': {
                'table_name': 'assessment_questionset',
                'model_name': 'QuestionSet',
                'columns':  ['set_id','user_id','n_questions','is_completed','score',],
                'attributes': ['INT PRIMARY KEY NOT NULL AUTO_INCREMENT', 'INT', 'INT', 'BOOLEAN', 'INT',]
            },  
            #selected_option,is_correct,set_id,question
            base_dir + '\\static\\csv\\userresponse.csv': {
                'table_name': 'assessment_userresponse',
                'model_name': 'UserResponse',
                'columns':  ["response","selected_option","is_correct","set_id","question_id","is_answered",],
                # add default values for response and is_answered
                'attributes' : ["INT PRIMARY KEY NOT NULL AUTO_INCREMENT","INT", "BOOLEAN", "INT", "INT","BOOLEAN"]
            },
        }
        
        cursor = connection.cursor()
        
       
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

            # Load data from CSV
            with open(csv_file_path, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    columns = ', '.join(row.keys())
                    placeholders = ', '.join(['%s'] * len(row))
                    query = f"INSERT INTO {table_info['table_name']} ({columns}) VALUES ({placeholders})"
                    cursor.execute(query, tuple(row.values()))
                    
        connection.commit()
        cursor.close()
        connection.close()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))


print("Database created successfully")