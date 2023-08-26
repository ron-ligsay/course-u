# your_app/management/commands/save_tables_to_json.py
import json
from django.core.management.base import BaseCommand
from website.models import YourModel1, YourModel2  # Import your models

class Command(BaseCommand):
    help = 'Save data from tables to JSON files'

    def handle(self, *args, **options):
        data = {}

        # Fetch data from each model and add it to the data dictionary
        data['model1'] = list(YourModel1.objects.values())
        data['model2'] = list(YourModel2.objects.values())

        # Save data as JSON files
        for model_name, model_data in data.items():
            json_file_path = f'{model_name}.json'
            with open(json_file_path, 'w') as file:
                json.dump(model_data, file, indent=4)
            self.stdout.write(self.style.SUCCESS(f'Data from {model_name} saved to {json_file_path}'))
