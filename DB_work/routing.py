from django.urls import path

from .consumers import WSConsumer

ws_urlpatterns = [
    path('home/flights/', WSConsumer.as_asgi())
]