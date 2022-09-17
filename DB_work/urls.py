from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('callsign', views.check_by_callsign, name='check_by_callsign'),
    path('flights', views.get_info, name='flights'),
    path('', views.firstpage, name='home'),
    path('login', views.check, name='check'),
    path('about', views.about_page, name ='about'),
    path('flight_not_tracked', views.flight_not_tracked, name = 'flight_not_tracked'),
    path('statistic', views.statistic, name = 'statistic'),
]
