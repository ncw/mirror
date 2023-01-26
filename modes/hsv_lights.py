from .utils import hsv_to_rgb, byte_scale_rgb

class Mode:
    NAME = "HSV lights with the 3 knobs"
    def __init__(self, mirror):
        self.mirror = mirror
    def update(self):
        """
        Update mirror with the current state
        """
        h, s, v = self.mirror.knob(2), self.mirror.knob(1), self.mirror.knob(0)
        r, g, b = hsv_to_rgb(h, s, v)
        self.mirror.fill(byte_scale_rgb((r, g, b)))
        #print("r=%5.2f g=%5.2f b=%5.2f h=%5.2f s=%5.2f v=%5.2f" % (r, b, g, h, s, v))
