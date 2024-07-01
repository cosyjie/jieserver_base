from django.apps import AppConfig


class SystemauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'panel.systemauth'
    verbose_name = '通用验证权限模块'
    version = '0.0.1-alpha'
