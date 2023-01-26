"""
Controller for LED based infinity mirror
"""

import time
from machine import Pin, Timer
from neopixel import NeoPixel
import modes

# Constants
nleds = 34
pin = Pin(0)
update_freq_hz = 50             # how often we update the LEDs

# ADC guard band
adc_min = 512
adc_max = 65526-adc_min

# Control buttons
buttons = (
    Pin(20, Pin.IN, Pin.PULL_UP),
    Pin(21, Pin.IN, Pin.PULL_UP),
)

class Mirror:
    """
    Infinity Mirror with LEDs
    """
    def __init__(self):
        self._leds = NeoPixel(pin, nleds)
        self._leds.ORDER = (0, 1, 2, 3) # R G B W
        self.n = nleds
        self.adc = [ machine.ADC(i) for i in range (4) ]
        self.mode = None
        self.set_mode(len(modes.MODES)-1)
        self.buttons_state = [1, 1]
        self.buttons_pressed = [False, False]
    def __setitem__(self, index, value):
        """
        We use mirror[0] = color to set colours
        """
        if index < 0 or index >= self.n:
            return
        self._leds[index] = value
    def fill(self, col):
        """
        Set all the LEDs to col
        """
        for i in range(self.n):
            self._leds[i] = col
    def read_buttons(self):
        """
        Read the state of the buttons to self.buttons_pressed
        """
        for i in range(len(buttons)):
            old = self.buttons_state[i]
            new = buttons[i].value()
            self.buttons_pressed[i] = (old == 0 and new != 0)
            self.buttons_state[i] = new
    def update(self, t=None):
        """
        Update the LEDs

        Returns the desired delay
        """
        delay = self.mode.update()
        self._leds.write()
        self.read_buttons()
        if self.buttons_pressed[0]:
            self.set_mode(self.mode_number + 1)
        elif self.buttons_pressed[1]:
            self.set_mode(self.mode_number - 1)
        return delay
    def knob(self, i):
        """
        Read the ADC as a floating point number 0..1
        """
        x = self.adc[i].read_u16() - adc_min
        x = x / float(adc_max - adc_min)
        if x < 0:
            x = 0.0
        if x > 1.0:
            x = 1.0
        return x
    def set_mode(self, i):
        """
        Runs the mode given
        """
        i %= len(modes.MODES)
        self.mode_number = i
        self.mode = modes.MODES[i](self)
        print(self.mode.NAME)

def main():
    mirror = Mirror()
    # Update the mirror off a timer interrupt
    timer = Timer()
    timer.init(freq=update_freq_hz, mode=Timer.PERIODIC, callback=mirror.update)
    try:
        while True:
            time.sleep(1)
    except:
        timer.deinit()
        raise

if __name__ == "__main__":
    main()
