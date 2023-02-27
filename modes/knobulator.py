import random
import math

class Mode:
    NAME = "Knobulator"
    def __init__(self, mirror):
        self.mirror = mirror
        self.p = [0,0,0]
    def update(self):
        for i in range(self.mirror.n):
            rgb = [128+127*math.sin(math.radians((self.p[j] + i) * 360 / self.mirror.n)) for j in range(3)]
            self.mirror[i] = rgb
        for j in range(3):
            self.p[j] += self.mirror.knob(j) * 2 - 1
