from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from messaging import consumers  # Import your consumers
from channels.asgi import get_asgi_application  # Update this import
from channels.generic.websocket import WebsocketConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Update this line
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                # Add your WebSocket consumers here
                path("ws/some_path/", consumers.YourConsumer.as_asgi()),
            ]
        )
    ),
})