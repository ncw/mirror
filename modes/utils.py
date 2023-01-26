"""
Utilities for the display modes
"""

def byte_scale(x):
    """
    Scale a float 0..1 into an int 0..255
    """
    x = int(256*x)
    if x < 0:
        x = 0
    if x >= 255:
        x = 255
    return x

def byte_scale_rgb(x):
    """
    Scale a float (r, g, b) 0..1 into ints 0..255
    """
    r, g, b = x
    return (byte_scale(r), byte_scale(g), byte_scale(b))

def hsv_to_rgb(h, s, v):
    """Convert HSV 0..1 to RGB 0..1"""
    if s == 0.0: return (v, v, v)
    i = int(h*6.)
    if i >= 6:
        i = 5
    f = (h*6.)-i
    p = v*(1.-s)
    q = v*(1.-s*f)
    t = v*(1.-s*(1.-f))
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i >= 5: return (v, p, q)
