import argparse
import asyncio
import websockets
import threading
import uuid
from queue import Queue

from lib.game import Game


async def listen(url="ws://localhost:8765"):
    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            # Update game state based on message
            print(f"Received: {msg}")


def create_connection(url, uuid_str):
    asyncio.run(listen(url))


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
        threading.Thread(target=start_network, args=(options.server_url, uuid_str, listen_queue, broadcast_queue), daemon=True).start()
    Game()
