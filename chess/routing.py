from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<int:game_id>', consumers.MessageSocket.as_asgi()),
]