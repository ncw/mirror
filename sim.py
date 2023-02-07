#!/usr/bin/env python3

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
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
    def circle(self, surface, col, width):
        img = pygame.Surface((width, width))
        pygame.draw.circle(img, col, (width/2, width/2), width/2)
        surface.blit(img, (self.x - width/2, self.y - width/2), special_flags=pygame.BLEND_ADD)
    def draw(self, surface, col):
        self.circle(surface, col, led_width*1.6) # exaggerate LED size
        r, g, b = col
        self.circle(surface, (r*0.1, g*0.1, b*0.1), 30*led_width)
        self.circle(surface, (r*0.05, g*0.05, b*0.05), height/2)

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
        self._knob = [0.5, 0.5, 0.5]
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
                if shift_pressed:
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
            delay = 0
        time.sleep(delay)

    pygame.quit()

if __name__ == "__main__":
    main()
