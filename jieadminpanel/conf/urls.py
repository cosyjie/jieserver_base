from pathlib import Path
from django.apps import apps
from django.conf import settings
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from panel.systemauth import views

urlpatterns = [
    path('', views.PanelLoginView.as_view()),
    path('login/', views.PanelLoginView.as_view(), name='login'),
    path('logout/', views.PanelLogoutView.as_view(), name='logout'),
    path('home/', include('panel.panelhome.urls', namespace='panelhome')),
    path('systemtools/', include('panel.module_system.urls', namespace='module_system')),
    path('databases/', include('panel.module_database.urls', namespace='module_database')),
    path('appstore/', include('panel.appstore.urls', namespace='appstore')),
    path('envs/', include('panel.module_envs.urls', namespace='module_envs')),
]

urlpatterns += staticfiles_urlpatterns()

# for app_name in settings.APPS_LIST:
#     app_dependent_modules = apps.get_app_config(app_name).dependent_modules
#     if app_dependent_modules is None or len(app_dependent_modules) == 0:
#         urlpatterns.append(path(f'{app_name}/', include(f'apps.{app_name}.urls', namespace=app_name)))