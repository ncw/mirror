"""
Controller for LED based infinity mirror
"""

import time
from machine import Pin, Timer
from neopixel import NeoPixel
import modes
import secrets
import network
import ntptime

# Constants
nleds = 34
pin = Pin(0)
update_freq_hz = 25             # how often we update the LEDs

# TZ is the base timezone offset from UTC in hours, 0 for UK, 1 for Europe etc.
TZ = 0

# ADC guard band
adc_min = 512
adc_max = 65526-adc_min

# Control buttons
buttons = (
    Pin(20, Pin.IN, Pin.PULL_UP),
    Pin(21, Pin.IN, Pin.PULL_UP),
)

# Where to save the current state
state_file = "state.txt"

# Wait this long before saving the file after changes
save_after_delay = update_freq_hz * 5

def local_time_offset():
    """
    Return the daylight savings time offset in hours for UK & Europe.

    This is incorrect for US.

    Adapted from: https://forum.micropython.org/viewtopic.php?f=2&t=4034 by JumpZero
    """
    year = time.localtime()[0]              # get current year
    HHMarch   = time.mktime((year,3 ,(31-(int(5*year/4+4))%7),1,0,0,0,0,0)) # Time of March change to Summer Time
    HHOctober = time.mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0)) # Time of October change to Winter Time
    now = time.time()
    if now < HHMarch :                    # we are before last sunday of March
        offset = 0
    elif now < HHOctober :                # we are before last sunday of October
        offset = 1
    else:                                 # we are after last sunday of October
        offset = 0
    return offset

class Mirror:
    """
    Infinity Mirror with LEDs
    """
    def __init__(self):
        self._leds = NeoPixel(pin, nleds)
        self._leds.ORDER = (0, 1, 2, 3) # R G B W
        self.n = nleds
        self.adc = [ machine.ADC(i) for i in range (5) ]
        self.mode = None
        self.load_state()
        self.buttons_state = [1, 1]
        self.buttons_pressed = [False, False]
        self.save_counter = 0
        self.temp = None
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(secrets.SSID, secrets.PASSWORD)
        self.time_set = False
        self.time_offset = 0
    def __setitem__(self, index, value):
        """
        We use mirror[0] = color to set colours
        """
        if index < 0 or index >= self.n:
            return
        self._leds[index] = value
    def __getitem__(self, index):
        """
        Read the value set back
        """
        if index < 0 or index >= self.n:
            return (0,0,0)
        return self._leds[index]
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
        self.mode.update()
        self._leds.write()
        self.read_buttons()
        if self.buttons_pressed[0]:
            self.set_mode(self.mode_number + 1)
        elif self.buttons_pressed[1]:
            self.set_mode(self.mode_number - 1)
        # Save the state after it has stopped changing
        if self.save_counter > 0:
            self.save_counter -= 1
            if self.save_counter == 0:
                self.save_state()
        # Set the time if unset
        if not self.time_set and self.wlan.isconnected():
            try:
                ntptime.settime()
            except Exception as e:
                print("Failed to set time:", e)
                return
            self.time_set = True
            self.time_offset = local_time_offset() + TZ*3600
            print("UTC Time:   %s" % (time.localtime(),))
            print("Local Time: %s" % (self.local_time(),))
    def local_time(self):
        """
        Returns the broken down local time
        """
        if not self.time_set:
            return (2023, 1, 1, 0, 0, 0, 0, 0, 0)
        now = time.time()
        return time.localtime(now+self.time_offset)
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
    def knob_brightness(self):
        """
        Brightness knob
        """
        return self.knob(0)
    def knob_hue(self):
        """
        Hue knob
        """
        return self.knob(1)
    def knob_speed(self):
        """
        Speed knob
        """
        return self.knob(2)
    def temperature(self):
        """
        Return the temperature of the board in C as a floating point number
        """
        volts = 3.3 * self.adc[4].read_u16() / 65536
        temp = 27 - (volts - 0.706)/0.001721
        if self.temp is None:
            self.temp = temp
        else:
            # Low pass the temperature with a time constant of approx one second
            self.temp = (self.temp * (update_freq_hz - 1) + temp) / update_freq_hz
        return self.temp
    def set_mode(self, i):
        """
        Runs the mode given
        """
        i %= len(modes.MODES)
        self.mode_number = i
        self.mode = modes.MODES[i](self)
        print(self.mode.NAME)
        self.save_counter = save_after_delay
    def load_state(self):
        """
        Load the state from a file
        """
        mode = 0
        try:
            with open(state_file) as f:
                mode = int(f.read())
        except Exception as e:
            print("Error reading file", e)
        self.saved_state = mode
        print("Loaded state")
        self.set_mode(mode)
    def save_state(self):
        """
        Save the state to a file
        """
        if self.saved_state == self.mode_number:
            return
        try:
            with open(state_file, "w") as f:
                f.write(str(self.mode_number))
        except Exception as e:
            print("Error writing file", e)
        self.saved_state = self.mode_number
        print("Saved state")

def main():
    mirror = Mirror()
    # Update the mirror at update_freq_hz
    tick_interval = int(1000/update_freq_hz)
    next_tick = time.ticks_add(time.ticks_ms(), tick_interval)
    while True:
        mirror.update()
        now = time.ticks_ms()
        sleep_time = time.ticks_diff(next_tick, now)
        if sleep_time < 0:
            print("Dropped frame by", -sleep_time, "ms")
            next_tick = now
        else:
            time.sleep_ms(sleep_time)
        next_tick = time.ticks_add(next_tick, tick_interval)

if __name__ == "__main__":
    main()
