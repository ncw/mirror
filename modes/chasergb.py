import random

class Chaser:
    def __init__(self, mirror):
        self.mirror = mirror
        self.pos = random.randrange(0, self.mirror.n)
        self.intensity = 1
        self.speed = (random.random() + 0.1) * random.choice((-1,1))
        self.type = random.randrange(0,3)
        self.fade = 0.89 + random.random() / 10.0
    def update(self, speed):
        self.intensity *= self.fade
        if self.intensity < 0.1:
            return False
        self.pos += self.speed * (speed + 0.5)
        if self.pos >= self.mirror.n:
            self.pos -= self.mirror.n
        if self.pos < 0:
            self.pos += self.mirror.n
        return True
    
class Mode:
    NAME = "Chase RGB"
    def __init__(self, mirror):
        self.mirror = mirror
        self.i = 0
        self.tick = 0
        self.chasers = []
        self.c = [[0,0,0] for i in range(self.mirror.n)]
    def update(self):
        hue, speed, bright = self.mirror.knob_hue(), self.mirror.knob_speed(), self.mirror.knob_brightness()
        self.mirror.fill((0,0,0))
        if len(self.chasers) < 4:
            self.chasers.append(Chaser(self.mirror))
        c2 = []
        for chaser in self.chasers:
            if chaser.update(speed):
                c2.append(chaser)
            self.c[int(chaser.pos)][chaser.type] += chaser.intensity
        b = bright * 256
        for i, c in enumerate(self.c):
            self.mirror[i] = int(min(255,(c[0] * b))),int(min(255,(c[1] * b))),int(min(255,(c[2] * b)))
            for j in range(3):
                self.c[i][j] *= (0.89 + hue / 10.0)
        self.chasers = c2
