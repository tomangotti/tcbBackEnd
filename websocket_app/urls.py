from django.urls import path
from .consumers import YourWebSocketConsumer

urlpatterns = [
    path("ws/send_message/", YourWebSocketConsumer.as_asgi()),
]