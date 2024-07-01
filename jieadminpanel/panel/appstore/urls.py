from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'appstore'

urlpatterns = [
    # path('init/', login_required(views.setup), name='init'),
    path('list/', login_required(views.AppStoreListView.as_view()), name='list'),
    path('app/detail/<int:pk>/', login_required(views.AppDetailView.as_view()), name='detail'),
    path('app/install/<int:pk>/', login_required(views.AppInstallView.as_view()), name='install'),
    path('apps/disabled/<int:pk>/', login_required(views.AppDisabledView.as_view()), name='disabled'),
    path('app/restore/<int:pk>/', login_required(views.AppRestoreView.as_view()), name='restore'),
    path('app/uninstall/<int:pk>/', login_required(views.AppUninstallView.as_view()), name='delete'),

    # path('app/action/<int:pk>/<str:action>/', login_required(views.AppActionView.as_view()), name='action'),
]