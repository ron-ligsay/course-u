from django.core.management.base import BaseCommand
import csv
import os
import mysql.connector
from website.models import Specialization, Test  # Import your models


class Command(BaseCommand):
    help = 'Import data from CSV files to MySQL database'
    
    def handle(self, *args, **options):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sql2023',
            database='courseu_db',
        )

        base_dir = os.getcwd()
        csv_table_mapping = {
        #    base_dir + '\static\csv\specialization.csv': {
        #         'table_name': 'website_specialization',
        #         'model_name': 'Specialization',
        #         'columns': ['specialization_id', 'field_id', 'title','description','roadmap_id',] 
        #     },
        #     base_dir + '\\static\\csv\\test.csv': {
        #         'table_name': 'website_test',
        #         'model_name': 'Test',
        #         'columns': ['question_id', 'question','option1','option2','option3','option4','answer','topic',]
        #     },
             base_dir + '\\job_post_scrapy\\jobs\\jobs_clean.csv': {
                'table_name': 'website_jobposting',
                'model_name': 'JobPosting',
                #link,keyword,title,company,company_link,date,link_clean,id
                'columns': ['link','keyword','title','company','company_link','date','link_clean','id']
            }
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
                # ... (create the table)
                columns = ', '.join([f"{col} VARCHAR(255)" for col in table_info['columns']])
                query = f"CREATE TABLE IF NOT EXISTS {table_info['table_name']} ({columns});"
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