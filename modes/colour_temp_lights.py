# Colour temperatures from http://planetpixelemporium.com/tutorialpages/light.html
color_temps = (
    ( 1900, (255, 147,  41)), # Candle
    ( 2600, (255, 197, 143)), # 40W Tungsten
    ( 2850, (255, 214, 170)), # 100W Tungsten
    ( 3200, (255, 241, 224)), # Halogen
    ( 5200, (255, 250, 244)), # Carbon Arc
    ( 5400, (255, 255, 251)), # High Noon Sun
    ( 6000, (255, 255, 255)), # Direct Sunlight
    ( 7000, (201, 226, 255)), # Overcast Sky
    (20000, ( 64, 156, 255)), # Clear Blue Sky
)
min_temp = 1900
max_temp = 20000

def k_to_rgb(k):
    """
    Calculate the rgb value for the given colour temperature
    """
    k = max(k, min_temp)
    k = min(k, max_temp)
    for i in range(len(color_temps)):
        k_1, rgb_1 = color_temps[i]
        if k_1 > k:
            k_0, rgb_0 = color_temps[i-1]
            delta_k = k_1 - k_0
            fraction_1 = (k - k_0) / delta_k
            fraction_0 = 1 - fraction_1
            r = fraction_0 * rgb_0[0] + fraction_1 * rgb_1[0]
            g = fraction_0 * rgb_0[1] + fraction_1 * rgb_1[1]
            b = fraction_0 * rgb_0[2] + fraction_1 * rgb_1[2]
            return (int(r), int(g), int(b))
    return color_temps[-1][1]

class Mode:
    NAME = "Lights with controllable colour temperature"
    def __init__(self, mirror):
        self.mirror = mirror
    def update(self):
        """
        Update mirror with the current state
        """
        k, _, v = self.mirror.knob(2)*(max_temp-min_temp)+min_temp, self.mirror.knob(1), self.mirror.knob(0)
        r, g, b = k_to_rgb(k)
        self.mirror.fill((int(r*v), int(g*v), int(b*v)))
        #print("k=%8.1f r=%3d g=%3d b=%3d" % (k, r, b, g))
