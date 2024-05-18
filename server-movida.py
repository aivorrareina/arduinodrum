import asyncio
import pickle
from alsa_midi import (AsyncSequencerClient, READ_PORT, WRITE_PORT,
                       NoteOnEvent, NoteOffEvent)


BOMBO_NORMAL = 60 #C2
CAJA_NORMAL = 62 #D2
HOST = '0.0.0.0'
PORT = 8888
MIDI_CLIENT_NAME = 'movida'

clients = []

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    print(f"Client connected: {addr}")
    clients.append(writer)

    try:
        while True:
            data = await reader.read(1)  # Read one byte of data
            if not data:
                break
            await broadcast(data)
    except asyncio.CancelledError:
        pass
    finally:
        print(f"Client disconnected: {addr}")
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()

async def broadcast(message):
    serialized_message = pickle.dumps(message)
    for client in clients:
        client.write(serialized_message)
        await client.drain()  # Ensure message is sent

async def handle_event(event):
    if isinstance(event, NoteOnEvent):
        await broadcast(event)

async def start_server(host, port):
    server = await asyncio.start_server(handle_client, host, port)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

async def show_input(client):
    port = client.create_port("inout", WRITE_PORT)
    while True:
        event = await client.event_input()
        await handle_event(event)

async def main():
    client = AsyncSequencerClient(MIDI_CLIENT_NAME)
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 8888       # Port to listen on

    await asyncio.gather(
        start_server(host, port),
        show_input(client)
    )

if __name__ == '__main__':
    asyncio.run(main())
