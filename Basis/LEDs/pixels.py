import math
import threading
import time

from gpiozero import LED

from Basis.LEDs import apa102 # pylint: disable=import-error

PINK = 0x7C1645
LILA = 0x8F20B6

class LEDSteuerung(object):
    def __init__(self):
        self.strip = apa102.APA102(12, 10)

        self.powerOn()
        self.clearStrip()

    def powerOn(self):
        self.power = LED(5)
        self.power.on()

    def clearStrip(self):
        self.strip.clear_strip()
        self.strip.show()

    def wakeup(self):
        for x in range(30):
            self.strip.rotate(1)
            brightness = min(x*5, 100)
            self.strip.set_pixel_rgb(0, PINK, bright_percent=brightness)
            self.strip.set_pixel_rgb(6, PINK, bright_percent=brightness)
            self.strip.show()
            time.sleep(0.03)

    def think(self):
        for x in range(30):
            self.strip.set_pixel_rgb(x%12, PINK)
            self.strip.set_pixel_rgb((6+x)%12, LILA)
            self.strip.show()
            time.sleep(0.08)

    def speak(self):
        for x in range(6):
            self.strip.set_pixel_rgb(x*2, PINK)
            self.strip.show()
            time.sleep(0.05)
            self.strip.set_pixel_rgb(x*2+1, LILA)
            self.strip.show()
            time.sleep(0.05)

        for x in range(900):
            brightness = abs(math.cos(math.radians(1*x))*80)+20
            for x in range(6):
                self.strip.set_pixel_rgb(x*2, PINK, bright_percent=brightness)
                self.strip.set_pixel_rgb(x*2+1, LILA, bright_percent=brightness)
            self.strip.show()
            time.sleep(0.01)

    def sleep(self):
        for x in range(16):
            brightness = max(100 - x*16, 0)
            self.strip.set_pixel_rgb(x%12, PINK, bright_percent=brightness)
            self.strip.set_pixel_rgb((6+x)%12, LILA, bright_percent=brightness)
            self.strip.show()
            time.sleep(0.05)
