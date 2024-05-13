import time
import alsa_midi as alsa
from alsa_midi.event import MIDI_BYTES_EVENTS,EventType
from time import sleep
import signal
import sys

client = alsa.SequencerClient("movida")
port = client.create_port("inout", alsa.WRITE_PORT)

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


signal_handler = SignalHandler()

print("Empezamos a escuchar")
while signal_handler.can_run():
    event = client.event_input(prefer_bytes=True)
    if event:
        type = None
        if event.type == EventType.NOTEON:
            print("Detalle {}".format(event.midi_bytes))            
            print("NOTA {}.{}".format(event.midi_bytes[0],event.midi_bytes[1],event.midi_bytes[2]))


