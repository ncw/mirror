from .utils import hsv_to_rgb
from math import sin, pi

class Mode:
    NAME = "HSV spin"
    def __init__(self, mirror):
        self.mirror = mirror
        self.t = 0
    def update(self):
        """
        Update mirror with the current state
        """
        v = self.mirror.knob(0)
        s = self.mirror.knob(1)
        speed = self.mirror.knob(2)
        speed = speed*speed*0.1
        for i in range(self.mirror.n):
            h = i / self.mirror.n + self.t
            if h > 1.0:
                h -= 1.0
            r, g, b = hsv_to_rgb(h, s, v)
            self.mirror[i] = (int(255*r), int(255*g), int(255*b))
        self.t += speed
        if self.t > 1.0:
            self.t -= 1.0
