import time
from math import sin, pi

class Mode:
    NAME = "Soft changing glow"
    def __init__(self, mirror):
        self.mirror = mirror
        self.state = 0
        self.t = 0
        self.delay = 0
    def scol(self, t, brightness):
        return (
            int((sin(3*t)+1)*127*brightness),
            int((sin(5*t)+1)*127*brightness),
            int((sin(7*t)+1)*127*brightness),
        )
    def update(self):
        """
        Update mirror with the current state
        """
        if self.delay:
            self.delay -= 1
            return
        if self.state == 0:
            self.mirror.fill((255,0,0))
            self.state += 1
            self.delay = 25
        elif self.state == 1:
            self.mirror.fill((0,255,0))
            self.state += 1
            self.delay = 25
        elif self.state == 2:
            self.mirror.fill((0,0,255))
            self.state += 1
            self.delay = 25
        elif self.state == 3:
            for i in range(0, self.mirror.n, 5):
                self.mirror[i+0] = (255,0,0)
                self.mirror[i+1] = (0,255,0)
                self.mirror[i+2] = (0,0,255)
                self.mirror[i+3] = (255,255,0)
                self.mirror[i+4] = (0,255,255)
            self.state += 1
            self.delay = 25
        else:
            brightness = self.mirror.knob_brightness()
            for i in range(self.mirror.n):
                self.mirror[i] = self.scol(self.t+0.05*i, brightness)
            self.t += 0.003
            if self.t > 2*pi:
                self.t -= 2*pi
            #self.delay = 5
