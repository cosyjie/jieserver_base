from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'panelhome'

urlpatterns = [
    path('index/', login_required(views.SystemHomeView.as_view()), name='index'),
    path('system/', login_required(views.system_state_view), name='systemState'),
    path('hostname/', login_required(views.HostnameView.as_view()), name='hostname'),
    path('timezone/', login_required(views.TimezoneView.as_view()), name='timezone'),

]
