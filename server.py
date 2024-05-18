#!/usr/bin/env /home/angel/arduinodrum/venv/bin/python3
import time
import alsa_midi as alsa
from alsa_midi.event import MIDI_BYTES_EVENTS,EventType
from time import sleep
import signal
import sys
import asyncio
import socket

BOMBO_NORMAL = 60 #C2
CAJA_NORMAL = 62 #D2
HOST = '0.0.0.0'
PORT = 8888
MIDI_CLIENT_NAME = 'movida'

class SignalHandler:
    shutdown_requested = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.request_shutdown)
        signal.signal(signal.SIGTERM, self.request_shutdown)

    def request_shutdown(self, *args):
        print('Request to shutdown received, stopping')
        self.shutdown_requested = True
        sys.exit()

    def can_run(self):
        return not self.shutdown_requested

def initAlsa():
    print('Iniciamos Alsa...')
    client = alsa.SequencerClient(MIDI_CLIENT_NAME)
    port = client.create_port("inout", alsa.WRITE_PORT)
    return client

if __name__ == "__main__":
    client = initAlsa()

    signal_handler = SignalHandler()

    clients = []

    print("Ok")
    while signal_handler.can_run():
        event = client.event_input(prefer_bytes=True)
        if event:
            type = None
            if event.type == EventType.NOTEON:
                if (event.midi_bytes[1] == BOMBO_NORMAL):
                    print("BOMBO")
                if (event.midi_bytes[1] == CAJA_NORMAL):
                    print("CAJA")