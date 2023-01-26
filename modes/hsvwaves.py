from .utils import hsv_to_rgb
from math import sin, pi

class Mode:
    NAME = "HSV Waves"
    def __init__(self, mirror):
        self.mirror = mirror
        self.t = 0
        self.h_multiplier = 3.123456
        self.s_multiplier = 7.398173
        self.v_multiplier = 5.393495
        self.h_angle = 0
        self.s_angle = 0
        self.v_angle = 0
    def hsv(self, offset, brightness):
        h = (sin(self.h_angle + offset*self.h_multiplier)**2)
        s = (sin(self.s_angle + offset*self.s_multiplier)**2)
        v = (0.75*((sin(self.v_angle + offset*self.v_multiplier)**2))+0.25) * brightness 
        r, g, b = hsv_to_rgb(h, s, v)
        return (int(255*r), int(255*g), int(255*b))
    def update(self):
        """
        Update mirror with the current state
        """
        brightness = self.mirror.knob(0)
        speed = self.mirror.knob(1)*0.01
        for i in range(self.mirror.n):
            self.mirror[i] = self.hsv(0.02*i, brightness)
        self.h_angle += self.h_multiplier * speed
        if self.h_angle > 2*pi:
            self.h_angle -= 2*pi
        self.s_angle += self.s_multiplier * speed
        if self.s_angle > 2*pi:
            self.s_angle -= 2*pi
        self.v_angle += self.v_multiplier * speed
        if self.v_angle > 2*pi:
            self.v_angle -= 2*pi
        self.t += 0.003
        if self.t > 2*pi:
            self.t -= 2*pi
