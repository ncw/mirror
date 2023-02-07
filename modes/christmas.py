from .utils import hsv_to_rgb, byte_scale_rgb
from math import sin, pi
import random

class Mode:
    NAME = "Christmas"
    def __init__(self, mirror):
        self.mirror = mirror
        self.angle = [ 2*pi*random.random() for i in range(self.mirror.n) ]
        self.speed = [ random.random() for i in range(self.mirror.n) ]
        self.hsv = [ self.col() for i in range(self.mirror.n) ]
    def col(self):
        """
        Pick a random christmassy (h, s, v)
        """
        if random.random() < 0.3:
            # Red range from actual LEDs
            h = random.uniform(0.0, 0.04)
            s = 1.0
        else:
            # Green range from actual LEDs
            h = random.uniform(0.25, 0.33)
            s = 1.0
        return (h, s, 1.0)
    def update(self):
        """
        Update mirror with the current state
        """
        brightness = self.mirror.knob_brightness()
        speed = self.mirror.knob_speed()*2.5+0.5
        for i in range(self.mirror.n):
            h, s, v = self.hsv[i]
            v = brightness * (sin(self.angle[i])**2)
            self.mirror[i] = byte_scale_rgb(hsv_to_rgb(h, s, v))
        for i in range(self.mirror.n):
            self.angle[i] += (1+self.speed[i])/50*speed
            if self.angle[i] > 2*pi:
                self.angle[i] -= 2*pi
                self.hsv[i] = self.col()
