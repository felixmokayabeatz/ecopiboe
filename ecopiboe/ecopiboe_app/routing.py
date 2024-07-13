# routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/piano/', consumers.PianoConsumer.as_asgi()),
]
