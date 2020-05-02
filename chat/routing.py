from chat import consumers

from django.urls import path

websocket_urlpatterns = [
    path('chat', consumers.ChatConsumer),
]