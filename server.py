import asyncio
import websockets

connected_clients = set()


async def handler(websocket):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast the received message to everyone
            websockets.broadcast(connected_clients, message)
    finally:
        connected_clients.remove(websocket)


async def main():
    # Start the server on localhost at port 8765
    async with websockets.serve(handler, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())