import asyncio
import pickle

async def handle_event(reader):
    while True:
        data = await reader.read(1024)  # Adjust buffer size as needed
        if not data:
            break
        event = pickle.loads(data)
        print(f"Received event: {event}")

async def tcp_client(host, port):
    reader, writer = await asyncio.open_connection(host, port)
    await handle_event(reader)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8888
    asyncio.run(tcp_client(host, port))
