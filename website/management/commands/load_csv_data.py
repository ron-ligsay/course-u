from django.core.management.base import BaseCommand
#from django.contrib.staticfiles import finders
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
        #for csv_file_path, table_info in zip(csv_file_paths, csv_table_mapping.values()):
            query = f"SHOW TABLES LIKE '{table_info['table_name']}'"
            cursor.execute(query)
            table_exists = cursor.fetchone() is not None

            if table_exists == False:
                print(f"Creating table '{table_info['table_name']}'...")
                csv_file = csv_file_path
                model_name = table_info['model_name']

                # Get the model class dynamically using globals()
                #model_class = globals()[model_name.capitalize()]
                model_class = globals()[model_name]

                if not model_class._meta.db_table:
                    self.stdout.write(self.style.ERROR(f"Table for model '{model_name}' doesn't exist. Creating table..."))
                    model_class._meta.db_table = model_class._meta.model_name
                    model_class._meta.managed = True
                    model_class._meta.db_table_created = True
                    model_class._meta.db_table_name = model_class._meta.db_table

                # with open(csv_file, 'r') as file:
                #     csv_reader = csv.DictReader(file)
                #     for row in csv_reader:
                #         model_class.objects.create(**row)
                #     self.stdout.write(self.style.SUCCESS(f'Data from {csv_file} loaded into {model_name} table'))

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