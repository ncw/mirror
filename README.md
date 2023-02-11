# Infinity Mirror Conversion

This is code to run the LEDs in an infinity mirror while running on a
Raspberry Pi Pico-W. It also contains a simulator for creating new
display modes.

![Infinity Mirror](images/mirror.gif?raw=true "Infinity Mirror")

The main files are as follows

- `mirror.py` - the main code to run on the pico
- `modes/` - a directory of "modes" for the mirror - edit `__init__.py` to add new ones
- `README.md` - this file
- `rp2mirror_boot` - set the pico to boot the code
- `rp2mirror_run` - send the code to the pico
- `rp2run` - run a bit of code on the pico
- `secrets.py` - contains WiFi access for the pico - not checked in
- `sim.py` - the simulator - run this to test the modes on your computer

Note that `secrets.py` should have your WiFi access details for use by the pico only.
    
```py
SSID = "yourssid"
PASSWORD = "your password"
```

## The mirror

The infinity mirror has a half silvered mirror and a fully silvered
mirror about 3 cm apart. Around the edge of that gap there are 34
neopixels controlled by the pico. The pico also has three analogue
potentiometers (knobs) which have the function:

0. Brightness
1. Hue
2. Speed

These can be interpreted by the running mode however its wants, but it
should try to obey the `Brightness` knob so as not to suprise the
user.

There are two buttons also, mode forward and mode backwards.

## Modes

The current installed modes are

- `colour_temp_lights` - all lights on at an adjustable colour temperature
- `hsv_lights` - all lights on with an adjustable Hue, Saturation and Value
- `hsvwaves` - waves of HSV around the lights
- `led_test` - turns one LED on at a time
- `softglow` - soft RGB glow
- `hsv_spin` - spinning Hue with controllable saturation and speed
- `christmas` - red and green christmassy lights
- `temperature` - shows the temperature. Number of on LEDs is temp in C with flashing showing partial.
- `time` - shows analogue time with 3 LEDS - Red is Hours, Green is Mins, Blue is Seconds

## Using the simulator

First make sure you have pygame installed.

Then run `python3 sim.py` to run the simulator.

You can control the simulator with the mouse

- Click LEFT, RIGHT to change mode
- Mouse wheel to change brightness (knob 0)
- SHIFT mouse wheel for hue (knob 1)
- CTRL mouse wheel for speed (knob 2)
- SHIFT+CTRL mouse wheel for temperature

## Writing a new mode

To write a new mode, copy and rename one of the existing ones and add
it to `modes/__init.py` in the order that you want it.

Note that the modes run under both python3 and micropython so a little
care is needed. Test first with the simulator.

Each mode should have this structure:

```py
class Mode:
    NAME = "Name of your mode - printed to the serial console"
    def __init__(self, mirror):
        self.mirror = mirror
        # more stuff
    def update(self):
        """
        Update mirror with the current state

        This is called 25 times per second.
        """
        # Plot your mode on the LEDs here
```

The mode is passed in a `mirror` object which has the following
methods you can use. This is a different object when running under
micropython or the simulator, but python's duck typing takes care of
it.

```py
class Mirror:
    def __setitem__(self, index, value):
        """
        We use mirror[0] = color to set colours
        """
    def __getitem__(self, index):
        """
        Read the value set by __setitem__
        """
    def fill(self, col):
        """
        Set all the LEDs to col
        """
    def local_time(self):
        """
        Returns the broken down local time like time.localtime()
        """
    def knob(self, i):
        """
        Read the ADC as a floating point number 0..1
        """
    def knob_brightness(self):
        """
        Brightness knob as a floating point number 0..1
        """
    def knob_hue(self):
        """
        Hue knob as a floating point number 0..1
        """
    def knob_speed(self):
        """
        Speed knob as a floating point number 0..1
        """
    def temperature(self):
        """
        Return the temperature of the board in C as a floating point number
        """
```

The `Mirror` object also has an attribute `n` which is the number of LEDs.

Note that colours are specified as tuples `(red, green, blue)` and the
range should be from `0..255` for each value.

## Build notes

Here is a collection of notes made while building the project.

### Micropython

Install micropython firmware from here

https://www.raspberrypi.com/documentation/microcontrollers/micropython.html

Note using Pico W version rp2-pico-w-20230116-unstable-v1.19.1-803-g1583c1f67.uf2

### rshell

rshell to communicate with Pico W and send / receive files.

    sudo apt install python3-rshell
    
Could also use Thonny.

rshell - can cp things to /pyboard

### Micropython test

Use `repl` then type

```
import machine
led = machine.Pin("LED", machine.Pin.OUT)
led.off()
led.on()
```

Micropython quick start docs are here: https://docs.micropython.org/en/latest/rp2/quickref.html

### Neopixel

RP2 micropython comes with built in neopixel library

This should set the LED to a pink color

```
from neopixel import NeoPixel
import machine
pin = machine.Pin(0)
pixels = NeoPixel(pin, 1)
pixels.fill((255, 5, 20))
pixels.write()
```

The ordering of RGB seems to be wrong - this is easily fixed with

    NeoPixel.ORDER = (0, 1, 2, 3)

So

```
from neopixel import NeoPixel
NeoPixel.ORDER = (0, 1, 2, 3)
import machine
pin = machine.Pin(0)
pixels = NeoPixel(pin, 1)
pixels.fill((255, 5, 20))
pixels.write()
```

### Booting

To start a python program at boot copy it as `main.py` using rshell

```
home/ncw> cp /pyboard/softglow.py /pyboard/main.py
Copying '/pyboard/softglow.py' to '/pyboard/main.py' ...
```

The pico will now run this program on powerup and rshell will no longer work.

#### Make rshell work again after main.py

If `rshell` is not working because a `main.py` has been installed.

Use

    picocom /dev/ttyACM0 -b115200

Then press CTRL-C until you see

```
Traceback (most recent call last):
  File "main.py", line 27, in <module>
KeyboardInterrupt: 
MicroPython v1.19.1-803-g1583c1f67 on 2023-01-16; Raspberry Pi Pico W with RP2040
Type "help()" for more information.
>>> 
```

Then type this to remove the `main.py`

```
import os
os.listdir("/")
os.remove("main.py")
```

Then enter CTRL-d to soft reset the pico.

CTRL-a CTRL-x to exit picocom

`rshell` should work again.

### Developing with rshell

Can use `rshell` interactively, but it can be scripted also

```
rshell --quiet cp softglow2.py /pyboard/softglow2.py
rshell --quiet "repl ~ exec(open('softglow2.py').read())"
```

This is embodied in the `rp2run` script.

### Power

From the data sheet

> VBUS is the 5V input from the micro-USB port, which is fed through a
> Schottky diode to generate VSYS. The VBUS to VSYS diode (D1) adds
> flexibility by allowing power ORing of different supplies into VSYS.

and later

> The simplest way to safely add a second power source to Pico is to
> feed it into VSYS via another Schottky diode (see Figure 15). This
> will 'OR' the two voltages, allowing the higher of either the
> external voltage or VBUS to power VSYS, with the diodes preventing
> either supply from back-powering the other.

We will run the LEDs directly from an external 5V power supply. Since
the RP SYS input range is 1.8V to 5.5V we don't need to worry about a
diode drop, so any silicon diode should be fine.

- So via a diode connect external 5V PSU to VSYS
- Leave VBUS unconnected (since it connects directly to the USB power)

This will allow us to connect a computer and not blow up the computer
with the external 5V PSU.

### WLAN

You will need to make a file called `secrets.py` to make the WLAN work
with the contents:

```
SSID = "your access point SSID"
PASSWORD = "you access point password"
```

This file isn't checked in to the repo and is in `.gitignore`.

### Current draw

The Board and LEDs take 1.22A with them all white on at maximum
brightness. With all the LEDs off the current draw is 30 mA. So each
LED is taking 35 mA maximum with the board taking 30 mA. Measured with
a 20A multimeter inline.

| Activity | Amps |
|----------|------|
| LEDs off | 0.03 |
| Time     | 0.07 |
| Temp     | 0.40 |
| Christmas | 0.30 |
| HSV Spin | 0.60 |
| All white | 1.22 |

The data sheet says

> Default output constant current value 12mA, high constant current
> accuracy, easy to reduce the power consumption of built-in lamp beads

Which aparently means 12mA **per** LED colour (Red, Green or blue) for
a total of 36 mA which agrees pretty well with the measured 35 mA.

This 12 mA per colour is quite obvious in a later table in the
datasheet (headings translated from Chinese).

| Luminous Color | Dominant Wavelength (nm) | Luminous Intensity (mcd) | Working Current (mA) | Working Voltage (V) |
|----|----|----|----|----|
|R|620-630| 600- 800|12|2.0-2.2|
|G|515-525|1300-2000|12|3.0-3.3|
|B|460-470| 400- 500|12|3.0-3.3|
