from django.apps import AppConfig


class ModuleDatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'panel.module_database'
    dependent_modules = []
    version = ''
    description = ''
