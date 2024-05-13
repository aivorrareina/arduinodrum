import time
import alsa_midi as alsa
from alsa_midi.event import MIDI_BYTES_EVENTS,EventType
from time import sleep

def midi_callback(timestamp, msg):
    print(f"Received MIDI message: {msg}")

client = alsa.SequencerClient("movida")
port = client.create_port("inout", alsa.WRITE_PORT)

print("Escuchando cosas")
while True:
    event = client.event_input(prefer_bytes=True)
    if event:
        type = None
        if event.type == EventType.NOTEON:
            print("Detalle {}".format(event.midi_bytes))            
            print("NOTA {}.{}".format(event.midi_bytes[0],event.midi_bytes[1],event.midi_bytes[2]))
