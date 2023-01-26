class Mode:
    NAME = "LED test"
    def __init__(self, mirror):
        self.mirror = mirror
        self.i = 0
        self.col = 0
        self.cols = ((255,0,0), (0,255,0), (0,0,255), (255,255,255))
        self.t = 0
    def update(self):
        """
        Update mirror with the current state
        """
        self.t += 1
        if self.t > 10:
            self.t = 0
        else:
            return
        self.mirror.fill((0,0,0))
        self.mirror[self.i] = self.cols[self.col]
        self.i += 1
        if self.i >= self.mirror.n:
            self.i = 0
            self.col += 1
            if self.col >= len(self.cols):
                self.col = 0
