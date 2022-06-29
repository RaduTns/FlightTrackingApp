from django.urls import path
from . import views

urlpatterns = [
    path('db', views.index, name='index'),
    path('callsign', views.check_by_callsign, name='check_by_callsign'),
    
]