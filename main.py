import json
import argparse
import asyncio
import websockets
import threading
import uuid
from queue import Queue

from lib.game import Game


async def listen(url, queue):
    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            queue.put(msg)
            print(f"Received: {msg}")


async def broadcast(url, queue):
    async with websockets.connect(url) as ws:
        while True:
            msg = queue.get()  # Blocking wait for message to send
            await ws.send(msg)
            print(f"Sent: {msg}")


def listen_handler(url, queue):
    asyncio.run(listen(url, queue))


def broadcast_handler(url, queue):
    asyncio.run(broadcast(url, queue))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server_url", help="URL of game server to connect to (e.g. ws://localhost:8765)", default=None)
    options = parser.parse_args()
    
    uuid_str = None
    listen_queue = None
    broadcast_queue = None 
    if options.server_url:
        uuid_str = str(uuid.uuid4())
        listen_queue = Queue()
        broadcast_queue = Queue()
        threading.Thread(target=listen_handler, args=(options.server_url, listen_queue), daemon=True).start()
        threading.Thread(target=broadcast_handler, args=(options.server_url, broadcast_queue), daemon=True).start()
    Game(uuid_str=uuid_str, listen_queue=listen_queue, broadcast_queue=broadcast_queue)
