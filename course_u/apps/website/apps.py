from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.website'

    # def ready(self):
    #         import your_app_name.signals  # Import your signals module

    #         # Connect the signal to the handler
    #         user_registered.connect(your_app_name.signals.send_welcome_email, sender=User)