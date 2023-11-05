# your_app/management/commands/create_superuser_prompt.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser through interactive prompt'

    def handle(self, *args, **options):
        username = input('Enter username: ')
        email = input('Enter email: ')
        password = input('Enter password: ')

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))
