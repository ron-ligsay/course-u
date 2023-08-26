# your_app/management/commands/load_csv_to_db.py
import os
import csv
from django.core.management.base import BaseCommand
from website.models import specialization  # Import your models

class Command(BaseCommand):
    help = 'Load CSV data into MySQL tables'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV file to load')
        parser.add_argument('--model', type=str, help='Model name', required=True)

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        model_name = options['model']

        # Get the model class dynamically using globals()
        #model_class = globals()[model_name.capitalize()]
        model_class = globals()[model_name]

        if not model_class._meta.db_table:
            self.stdout.write(self.style.ERROR(f"Table for model '{model_name}' doesn't exist. Creating table..."))
            model_class._meta.db_table = model_class._meta.model_name
            model_class._meta.managed = True
            model_class._meta.db_table_created = True
            model_class._meta.db_table_name = model_class._meta.db_table

        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                model_class.objects.create(**row)
            self.stdout.write(self.style.SUCCESS(f'Data from {csv_file} loaded into {model_name} table'))
