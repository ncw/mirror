# Infinity Mirror Conversion

## Micropython

Install micropython firmware from here

https://www.raspberrypi.com/documentation/microcontrollers/micropython.html

Note using Pico W version rp2-pico-w-20230116-unstable-v1.19.1-803-g1583c1f67.uf2

## rshell

rshell to communicate with Pico W and send / receive files.

    sudo apt install python3-rshell
    
Could also use Thonny.

rshell - can cp things to /pyboard

## Micropython test

Use `repl` then type

```
import machine
led = machine.Pin("LED", machine.Pin.OUT)
led.off()
led.on()
```

Micropython quick start docs are here: https://docs.micropython.org/en/latest/rp2/quickref.html

## Neopixel

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

## Alternative neopixel library

Alternative Neopixel library to run the LEDs WS2812 - no longer needed
as built in to RP2 micropython.

https://github.com/blaz-r/pi_pico_neopixel

Download neopixel.py

    git clone git@github.com:blaz-r/pi_pico_neopixel.git

from rshell copy the library to the pico

    cp pi_pico_neopixel/neopixel.py /pyboard/

Smoke test - from repl

    import neopixel

Quick test

```
from neopixel import Neopixel

pin = 0
pixels = Neopixel(1, 0, pin, "RGB")
pixels.fill((255, 5, 20))
pixels.show()
```

## Wiring

Can get 5V from VBUS pin - ok for small currents

## Booting

To start a python program at boot copy it as `main.py` using rshell

```
home/ncw> cp /pyboard/softglow.py /pyboard/main.py
Copying '/pyboard/softglow.py' to '/pyboard/main.py' ...
```

The pico will now run this program on powerup and rshell will no longer work.

### Make rshell work again after main.py

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

## Developing with rshell

Can use `rshell` interactively, but it can be scripted also

```
rshell --quiet cp softglow2.py /pyboard/softglow2.py
rshell --quiet "repl ~ exec(open('softglow2.py').read())"
```

This is embodied in the `rp2run` script.

## Power

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



