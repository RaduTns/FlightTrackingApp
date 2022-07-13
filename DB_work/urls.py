from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('db', views.index, name='index'),
    path('callsign', views.check_by_callsign, name='check_by_callsign'),
    path('flights', views.get_info, name='flights'),
    path('', views.firstpage, name='home'),
    path('login', views.check, name='check')
]