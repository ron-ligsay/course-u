from django.apps import AppConfig


class AcadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.acad'

    # def ready(self):
    #     import utilities.signal