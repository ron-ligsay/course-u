# your_app/management/commands/load_all_json_to_db.py
import os
import json
from django.core.management.base import BaseCommand
from website.models import specialization  # Import your models

class Command(BaseCommand):
    help = 'Load all JSON files from a directory into MySQL tables'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='Directory containing JSON files')

    def handle(self, *args, **options):
        directory = options['directory']
        json_files = [file for file in os.listdir(directory) if file.endswith('.json')]

        for json_file in json_files:
            with open(os.path.join(directory, json_file), 'r') as file:
                model_name = json_file.replace('.json', '')
                model_class = globals()[model_name.capitalize()]
                model_data = json.load(file)
                for item in model_data:
                    model_class.objects.create(**item)
            self.stdout.write(self.style.SUCCESS(f'Data from {json_file} loaded into {model_name} table'))
