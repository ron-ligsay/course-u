from django.core.management.base import BaseCommand
#from django.contrib.staticfiles import finders
import csv
import os
import mysql.connector

class Command(BaseCommand):
    help = 'Import data from CSV files to MySQL database'
    
    def handle(self, *args, **options):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sql2023',
            database='courseu_db',
        )
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_table_mapping = {
            # os.path.join(base_dir, 'static\\csv\\records.csv'): {
            #     'table_name': 'website_record',
            #     'columns': ['id', 'created_at', 'first_name','last_name','email','phone','address','city','state','zip_code']  # Replace with actual column names
            # },
            os.path.join(base_dir, '..\\static\\csv\\specialization.csv'): {
                'table_name': 'website_specialization',
                'columns': ['specialization_id', 'field_id', 'title','description','roadmap_id',] 
            }
        }
        
        cursor = connection.cursor()

        #csv_files = ['database/records.csv']  # List of your CSV files
        # csv_directory = finders.find('database')
        # csv_directory = finders.find('database')
       
        # csv_table_mapping = {
        #     'csv/records.csv': {
        #         'table_name': 'website_record',
        #         'columns': ['id', 'created_at', 'first_name','last_name','email','phone','address','city','state','zip_code']  # Replace with actual column names
        #     },
        #     # 'file2.csv': {
        #     #     'table_name': 'table2',
        #     #     'columns': ['col1_table2', 'col2_table2', ...]  # Replace with actual column names
        #     # },
        #     # Add more CSV files and corresponding table/column information
        # }

        #csv_file_paths = [finders.find(path) for path in csv_table_mapping.keys()]
        
        for csv_file_path, table_info in csv_table_mapping.items():
        #for csv_file_path, table_info in zip(csv_file_paths, csv_table_mapping.values()):
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