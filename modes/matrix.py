import random

class Mode:
    NAME = "Matrix"
    def __init__(self, mirror):
        self.mirror = mirror
        self.i = 0
        self.tick = 0
        self.y = [0,0]
        self.s = [0,0]
        self.c = [0] * self.mirror.n
    def update(self):
        hue, speed, bright = self.mirror.knob_hue(), self.mirror.knob_speed(), self.mirror.knob_brightness()
        self.mirror.fill((0,0,0))
        for i in range(2):
            if self.s[i] == 0 or self.y[i] > 100:
                self.s[i] = random.random()*4+1
                self.y[i] = 0
            y = int(self.y[i] * 11 / 100)
            if i == 0:
                y0 = 23 + y
            else:
                y0 = 16 - y
            self.c[y0] = 1
            self.y[i] += self.s[i] * (speed + 0.2)
        if self.tick == 0:
            self.c[random.randint(0,5)] = 1
            self.c[random.randint(17,22)] = 1
        for i, c in enumerate(self.c):
            self.mirror[i] = (0,int(c*255*bright),0)
            self.c[i] *= 0.95
        self.tick = (self.tick + 1) % 10
