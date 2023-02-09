from .utils import hsv_to_rgb, byte_scale_rgb

# Angle of each LED in degrees
#
# Made using sim.py - see commented out code in LED.__init__
led_angle = (
    204.2,
    195.1,
    185.1,
    174.9,
    164.9,
    155.8,
    145.5,
    139.3,
    131.1,
    120.2,
    106.2,
    90.0,
    73.8,
    59.8,
    48.9,
    40.7,
    34.5,
    24.2,
    15.1,
    5.1,
    354.9,
    344.9,
    335.8,
    325.5,
    319.3,
    311.1,
    300.2,
    286.2,
    270.0,
    253.8,
    239.8,
    228.9,
    220.7,
    214.5,
)

class Mode:
    NAME = "Show the current time"
    def __init__(self, mirror):
        self.mirror = mirror
        self.counter = 0
    def set(self, angle, col):
        """
        Set the LED nearest to angle to col where angle is fraction of a circle.

        The colour is added to any existing colour.
        """
        angle *= 360
        if angle < 0:
            angle += 360
        if angle >= 360:
            angle -= 360
        pos = 0
        best_diff = 1000
        for i in range(len(led_angle)):
            diff = abs(led_angle[i] - angle)
            if diff > 180:
                diff = 360 - diff
            if diff < best_diff:
                best_diff = diff
                pos = i
        r, g, b = self.mirror[pos]
        self.mirror[pos] = (r+col[0], g+col[1], b+col[2])
    def update(self):
        """
        Update mirror with the current state
        """
        t = self.mirror.local_time()
        h, m, s = t[3], t[4], t[5]
        brightness = 255 # int(255*self.mirror.knob_brightness())
        self.mirror.fill((0,0,0))
        
        # Hour hand
        if h >= 12:
            h -= 12
        h_pos = h / 12 + m / 60 / 12
        self.set(h_pos, (brightness, 0, 0))
        
        # Minute hand
        m_pos = m / 60 + s / 60 / 60
        self.set(m_pos, (0, brightness, 0))
        
        # Second hand
        s_pos = s / 60
        self.set(s_pos, (0, 0, brightness))
        
        self.counter += 1
