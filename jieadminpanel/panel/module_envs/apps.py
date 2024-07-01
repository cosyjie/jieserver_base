from django.apps import AppConfig


class ModuleEnvsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'panel.module_envs'
    verbose_name = '开发语言'
    version = '0.0.1-Alpha'
    description = '管理项目部署相关环境'
