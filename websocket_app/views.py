from django.shortcuts import render

import asyncio
import websockets

async def websocket_handler(websocket, path):
    while True:
        message = await websocket.recv()
        print(f"Received message: {message}")
        # Handle the message as needed

def start_websocket_server():
    start_server = websockets.serve(websocket_handler, "localhost", 3000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    start_websocket_server()