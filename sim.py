#!/usr/bin/env python3

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
#import pygame.gfxdraw
import time
import modes

# Dimensions measured from the mirror in mm
# The infinity mirror has 34 LEDs, 11 up each side and 6 on top and bottom

hleds = 6
hpadding = 37
width = 300

vleds = 11
vpadding = 34
height = 504

led_width = 5

update_freq_hz = 25             # how often we update the LEDs
    
class LED:
    """
    One of the Infinity Mirror's LEDs
    """
    def __init__(self, pos):
        self.pos = pos
        self.x, self.y = pos
        center_x = width/2
        center_y = height/2
        self.dx = (center_x - self.x)/32
        self.dy = (center_y - self.y)/32
        #print(self.dx, self.dy)
    def circle(self, surface, col, width, offset_x=0, offset_y=0):
        img = pygame.Surface((width, width))
        pygame.draw.circle(img, col, (width/2, width/2), width/2)
        w = int(width/2+0.5)
        #pygame.gfxdraw.filled_circle(img, w, w, w-1, col)
        #pygame.gfxdraw.aacircle(img, w, w, w, col)
        surface.blit(img, (self.x - width/2 + offset_x, self.y - width/2 + offset_y), special_flags=pygame.BLEND_ADD)
    def draw(self, surface, col):
        size = 1.0
        gap = 10*size
        brightness = 1.0
        r, g, b = col
        diffuse_width = width
        diffuse_brightness = 0.04
        # Can see 24 LEDs deep
        # Draw an LED and a diffuse beam for each LED
        for i in range(24):
            self.circle(surface, (brightness*r, brightness*g, brightness*b), led_width*size*1.4, offset_x=i*self.dx, offset_y=i*self.dy)
            if i % 4 == 0:
                self.circle(surface, (r*brightness*diffuse_brightness, g*brightness*diffuse_brightness, b*brightness*diffuse_brightness), diffuse_width*size, offset_x=i*self.dx, offset_y=i*self.dy)
                #self.circle(surface, (r*diffuse_brightness, g*diffuse_brightness, b*diffuse_brightness), diffuse_width*size, offset_x=i*self.dx, offset_y=i*self.dy)
            size *= 0.95
            brightness *= 0.90
        #self.circle(surface, (r*0.1, g*0.1, b*0.1), 30*led_width)
        #self.circle(surface, (r*0.05, g*0.05, b*0.05), height/2)

class Mirror:
    """
    Infinity Mirror with LEDs
    """
    def __init__(self):
        # LEDs in the mirror in the correct order
        hspacing = (width - 2*hpadding)/(hleds-1)
        vspacing = (height - 2*vpadding)/(vleds-1)
        leds = []
        for i in range(hleds):
            leds.append(LED((hspacing * i + hpadding, height)))
        for i in reversed(range(vleds)):
            leds.append(LED((width, vspacing * i + vpadding)))
        for i in reversed(range(hleds)):
            leds.append(LED((hspacing * i + hpadding, 0)))
        for i in range(vleds):
            leds.append(LED((0, vspacing * i + vpadding)))
        self._leds = leds
        self.n = len(leds)
        self._cols = [ (0,0,0) ] * self.n
        self._knob = [0.5, 0.5, 0.5, 0.6]
        self.mode = None
        self.set_mode(0)
    def __setitem__(self, index, value):
        """
        We use mirror[0] = color to set colurs
        """
        if index < 0 or index >= self.n:
            return
        self._cols[index] = value
    def fill(self, col):
        """
        Set all the LEDs to col
        """
        for i in range(self.n):
            self._cols[i] = col
    def update(self, screen):
        """
        Update the display

        Write the state of the LEDs to the screen

        Returns the desired delay
        """
        delay = self.mode.update()
        for i in range(self.n):
            self._leds[i].draw(screen, self._cols[i])
        return delay
    def knob(self, i):
        """
        Reads the value of knob i as 0..1
        """
        return self._knob[i]
    def knob_brightness(self):
        """
        Brightness knob
        """
        return self.knob(0)
    def knob_hue(self):
        """
        Hue knob
        """
        return self.knob(1)
    def knob_speed(self):
        """
        Speed knob
        """
        return self.knob(2)
    def temperature(self):
        """
        Return the temperature of the board in C as a floating point number
        """
        return self.knob(3)*34
    def add_knob(self, i, delta):
        """
        Changes the value of knob i by delta
        """
        self._knob[i] += delta
        if self._knob[i] > 1.0:
            self._knob[i] = 1.0
        if self._knob[i] < 0.0:
            self._knob[i] = 0.0
    def set_mode(self, i):
        """
        Runs the mode given
        """
        i %= len(modes.MODES)
        self.mode_number = i
        self.mode = modes.MODES[i](self)
        print(self.mode.NAME)
    def press_button(self, i):
        """
        Received a button press
        """
        if i == 0:
            self.set_mode(self.mode_number + 1)
        elif i == 1:
            self.set_mode(self.mode_number - 1)

def main():
    print("Click LEFT, RIGHT to change mode")
    print("Mouse wheel to change brightness (knob 0)")
    print("SHIFT mouse wheel for hue (knob 1)")
    print("CTRL mouse wheel for speed (knob 2)")
    print("SHIFT+CTRL mouse wheel for temperature")
    pygame.init()
    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Infinity Mirror Simulator")

    mirror = Mirror()

    quit = False
    shift_pressed = False
    control_pressed = False
    while not quit:
        start = time.time()
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                quit = True
            if e.type == pygame.KEYDOWN or e.type == pygame.KEYUP:
                if e.key == pygame.K_LSHIFT or e.key == pygame.K_RSHIFT:
                    shift_pressed = (e.type == pygame.KEYDOWN)
                elif e.key == pygame.K_LCTRL or e.key == pygame.K_RCTRL:
                    control_pressed = (e.type == pygame.KEYDOWN)
            if e.type == pygame.MOUSEBUTTONDOWN:
                knob_number = 0
                if shift_pressed and control_pressed:
                    knob_number = 3
                elif shift_pressed:
                    knob_number = 1
                elif control_pressed:
                    knob_number = 2
                if e.button == 1:
                    mirror.press_button(0)
                elif e.button == 3:
                    mirror.press_button(1)
                elif e.button == 4:
                    mirror.add_knob(knob_number, 0.05)
                elif e.button == 5:
                    mirror.add_knob(knob_number, -0.05)

        screen.fill((0,0,0))
        mirror.update(screen)
        pygame.display.update()
        dt = time.time() - start
        delay = 1.0/update_freq_hz - dt
        if delay < 0:
            #print(f"Dropped frame by {-delay*1000:.2f}ms")
            delay = 0
        time.sleep(delay)

    pygame.quit()

if __name__ == "__main__":
    main()
