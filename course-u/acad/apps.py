from django.apps import AppConfig


class AcadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acad'

    # def ready(self):
    #     import utilities.signal