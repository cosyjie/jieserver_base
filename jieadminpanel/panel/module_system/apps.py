from django.apps import AppConfig


class ModuleSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'panel.module_system'
    verbose_name = '系统工具模块'
    version = '0.0.1-Alpha'
    description = '操作系统管理工具'
