#!/usr/bin/env /home/angel/env/bin/python3
from subprocess import run
import sys
import alsa_midi as alsa

LGPT = '/home/angel/lgpt/bin/lgpt.rpi-exe'
DATABASE = "/home/angel/lgpt.data"
MIDI_PORT = 'movida'

def main():
  try:
    data = run(LGPT, capture_output=True, shell=True)
  except (EOFError, KeyboardInterrupt):
    sys.exit()

  output = data.stdout.splitlines()
  errors = data.stderr.splitlines()

  print('output')
  print(data.stdout)
  print('Errores')
  print(data.stderr)

  print(data.returncode)

def setup_midi():
  print('Inicializando midi...')
  client = alsa.SequencerClient("movida2")
  port = client.create_port("inout")
  print('Hecho.')
  
def restart_alsa():
  print('Restart Alsa...')
  run(["/etc/init.d/alsa-utils", "stop"])
  run(["/etc/init.d/alsa-utils", "start"])
  print('Hecho.')

if __name__ == "__main__":
  #restart_alsa()
  #setup_midi()
  main()