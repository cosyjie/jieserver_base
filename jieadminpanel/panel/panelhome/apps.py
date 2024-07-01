from django.apps import AppConfig


class PanelhomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'panel.panelhome'
    verbose_name = '控制面板基础'
    version = '0.0.1-Alpha'