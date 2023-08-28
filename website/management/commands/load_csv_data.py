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
                    unique_key = row[0]  # Use first column as unique key, Replace with the appropriate column name

                    # Check if row with unique key already exists
                    existing_record = model_class.objects.filter(*{table_info['columns'][0]: unique_key}).first()
                    
                    if existing_record:  # Replace with the appropriate column name
                        # Update existing record
                        for index, column in enumerate(table_info['columns'][1:]):
                            setattr(existing_record, column, row[index + 1])
                        existing_record.save()
                        self.stdout.write(self.style.SUCCESS(f"Record with key '{unique_key}' updated"))

                    else:
                        # Insert a new record
                        new_record = model_class(**dict(zip(table_info['columns'], row)))
                        new_record.save()
                        self.stdout.write(self.style.SUCCESS(f"Record with key '{unique_key}' inserted"))
                    # Prepare column names and values
                    # columns = ', '.join(table_info['columns'])
                    # placeholders = ', '.join(['%s'] * len(row))
                    # query = f"INSERT INTO {table_info['table_name']} ({columns}) VALUES ({placeholders})"
                    # cursor.execute(query, tuple(row))
                connection.commit()

        cursor.close()
        connection.close()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))


print("Database created successfully")