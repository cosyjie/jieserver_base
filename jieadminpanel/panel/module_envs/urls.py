from django.apps import apps
from django.urls import path, include
from django.conf import settings


app_name = 'module_envs'

urlpatterns = []

for app in settings.APPS_LIST:
    app_dependent_modules = apps.get_app_config(app).dependent_modules

    if app_name in app_dependent_modules:
        urlpatterns.append(path(f'{app}/', include(f'apps.{app}.urls', namespace=app)))