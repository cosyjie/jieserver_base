from django.apps import apps
from django.urls import path, include
from django.conf import settings
from app_files.conf.apps_enabled import APPS_LIST

app_name = 'module_system'

urlpatterns = []

for app in APPS_LIST:
    app_dependent_modules = apps.get_app_config(app).dependent_modules

    if app_name in app_dependent_modules:
        urlpatterns.append(path(f'{app}/', include(f'apps.{app}.urls', namespace=app)))
