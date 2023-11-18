
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from . import consumers  # Import your app's consumers
from django.urls import path

websocket_urlpatterns = [
    path("ws/send_message/", consumers.YourWebSocketConsumer.as_asgi()),
    # Add more paths if needed
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})