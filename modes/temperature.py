from .utils import hsv_to_rgb, byte_scale_rgb

class Mode:
    NAME = "Show the temperature"
    def __init__(self, mirror):
        self.mirror = mirror
        self.counter = 0
    def update(self):
        """
        Update mirror with the current state
        """
        temp = self.mirror.temperature()
        if self.counter % 25 == 0:
            print("%.1f" % temp)
        s = 1.0
        v = self.mirror.knob_brightness()
        
        # Colours
        # - Red  0.000 for hottest
        # - Blue 0.653 coolest
        #
        # If temperature is 15.3 degrees, put on 15 LEDs with the 16th one on 0.3 of the time.
        t0 = int(temp) - 1
        t1 = t0 + 1
        dt = temp - 1 - t0
        count = (self.counter % 25) / 25
        for i in range(self.mirror.n):
            j = self.mirror.n - 1 - i
            h = (j / self.mirror.n) * 0.653
            r, g, b = hsv_to_rgb(h, s, v)
            col = byte_scale_rgb((r, g, b))
            if i == t1:
                if count < dt:
                    self.mirror[j] = col
                else:
                    self.mirror[j] = (0,0,0)
            elif i <= t0:
                self.mirror[j] = col
            else:
                self.mirror[j] = (0,0,0)
        self.counter += 1
