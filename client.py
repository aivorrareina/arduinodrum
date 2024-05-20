import asyncio
import pickle
import time
import RPi.GPIO as GPIO

BOMBO = 17

async def activate_instrumento(ins):
    GPIO.output(ins, GPIO.HIGH)
    await asyncio.sleep(0.05)
    GPIO.output(ins, GPIO.LOW)


async def handle_event(reader):
    while True:
        try:
            data = await reader.read(1024)  # Adjust buffer size as needed
            if not data:
                print("Connection closed by the server")
                break
            event = pickle.loads(data)
            print(f"Received event: {event}")
            #await activate_instrumento(BOMBO)
        except Exception as e:
            print(f"Error handling event: {e}")
            break

async def tcp_client(host, port):
    while True:
        try:
            print(f"Attempting to connect to {host}:{port}")
            reader, writer = await asyncio.open_connection(host, port)
            print("Connected to server")
            await handle_event(reader)
        except (ConnectionRefusedError, ConnectionResetError, asyncio.TimeoutError) as e:
            print(f"Connection failed: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8888
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(BOMBO, GPIO.OUT)
    asyncio.run(tcp_client(host, port))
