import random

class Prey:
    def __init__(self, mode):
        self.mode = mode
        self.mirror = mode.mirror
        self.pos = random.randrange(0,self.mirror.n)
        self.n = 0
    def update(self):
        self.n -= 1
        if self.n <= 0:
            self.n = random.randrange(1,5)
            self.d = random.choice((-1,1))
        self.pos += self.d
        if self.pos < 0: self.pos += self.mirror.n
        if self.pos >= self.mirror.n: self.pos -= self.mirror.n
        dead = False
        for hunt in self.mode.hunt:
            if self.pos == hunt.pos:
                dead = True
        return not dead

class Hunt:
    def __init__(self, mode):
        self.mode = mode
        self.mirror = mode.mirror
        self.pos = random.randrange(0,self.mirror.n)
        self.n = 0
    def update(self):
        self.n -= 1
        if self.n > 0:
            return
        self.n = random.randrange(0,10)
        dmin = 1000
        s = 0
        for prey in self.mode.prey:
            d1 = (prey.pos - self.pos + self.mirror.n) % self.mirror.n
            d2 = self.mirror.n - d1
            if d1 < d2:
                if d1 < dmin:
                    dmin = d1
                    s = 1
            else:
                if d2 < dmin:
                    dmin = d2
                    s = -1
        if s:
            self.pos += s
            if self.pos < 0: self.pos += self.mirror.n
            if self.pos >= self.mirror.n: self.pos -= self.mirror.n
    
class Mode:
    NAME = "Hunter/Prey"
    def __init__(self, mirror):
        self.mirror = mirror
        self.i = 0
        self.tick = 0
        self.prey = []
        self.hunt = [ Hunt(self) for i in range(2) ]
        self.chance = 1.0
    def update(self):
        hue, speed, bright = self.mirror.knob_hue(), self.mirror.knob_speed(), self.mirror.knob_brightness()
        self.mirror.fill((0,0,0))
        if len(self.prey) < 4:
            if random.random() < self.chance or len(self.prey) == 0:
                self.prey.append(Prey(self))
        p2 = []
        for prey in self.prey:
            self.mirror[prey.pos] = (0,255,0)
            if prey.update():
                p2.append(prey)
            else:
                self.chance /= 2.0
        self.prey = p2
        for hunt in self.hunt:
            self.mirror[hunt.pos] = (255,0,0)
            hunt.update()
        self.chance *= 1.1
        if self.chance > 1.0:
            self.chance = 1.0
