import asyncio
import random
from bleak import BleakServer

# Define your custom service and characteristic UUIDs
SERVICE_UUID = "00000000-0000-0000-0000-000000000000"
CHARACTERISTIC_UUID = "00000000-0000-0000-0000-000000000001"

# Create a callback function for when a client connects
def on_connect(server: BleakServer, client: str):
    print(f"Client connected: {client}")

# Create a callback function for when a client disconnects
def on_disconnect(server: BleakServer, client: str):
    print(f"Client disconnected: {client}")

async def main():
    # Create the server and start advertising
    server = BleakServer(SERVICE_UUID, on_connect, on_disconnect)
    await server.start()

    try:
        while True:
            # Generate a random byte
            value = random.randint(0, 255).to_bytes(1, 'big')

            # Update the characteristic value
            await server.update_value(CHARACTERISTIC_UUID, value)

            # Wait for 1 second
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        # Stop advertising and shut down the server
        await server.stop()

# Run the main function in the asyncio event loop
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
