import json
from channels.generic.websocket import AsyncWebsocketConsumer

class YourWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect")
        await self.accept()

    async def disconnect(self, close_code):
        print("disconnect")
        pass

    async def receive(self, text_data):
        # Handle received data
        await self.send(text_data=json.dumps({'message': text_data}))