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
        #base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        base_dir = os.getcwd()
        csv_table_mapping = {
            # os.path.join(base_dir, 'static\\csv\\records.csv'): {
            #     'table_name': 'website_record',
            #     'columns': ['id', 'created_at', 'first_name','last_name','email','phone','address','city','state','zip_code']  # Replace with actual column names
            # },
           base_dir + '\static\csv\specialization.csv': {
                'table_name': 'website_specialization',
                'model_name': 'Specialization',
                'columns': ['specialization_id', 'field_id', 'title','description','roadmap_id',] 
            },
            base_dir + '\\static\\csv\\test.csv': {
                'table_name': 'website_test',
                'model_name': 'Test',
                'columns': ['question_id', 'question','option1','option2','option3','option4','answer','topic',]
            }
        }
        
        cursor = connection.cursor()
        
       
        for csv_file_path, table_info in csv_table_mapping.items():
            model_name = table_info['model_name']
            model_class = globals()[model_name]

            # Create table if it doesn't exist
            columns = ', '.join([f"{col} VARCHAR(255)" for col in table_info['columns']])
            query = f"CREATE TABLE IF NOT EXISTS {table_info['table_name']} ({columns});"
            cursor.execute(query)
            connection.commit()

            with open(csv_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                for row in reader:
                    # Prepare column names and values
                    columns = ', '.join(table_info['columns'])
                    placeholders = ', '.join(['%s'] * len(row))
                    query = f"INSERT INTO {table_info['table_name']} ({columns}) VALUES ({placeholders})"
                    cursor.execute(query, tuple(row))
                connection.commit()

        cursor.close()
        connection.close()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))


print("Database created successfully")