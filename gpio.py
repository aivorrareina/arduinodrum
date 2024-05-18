from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory(host='192.168.100.2')

red = LED(17,pin_factory=factory)

red.off()