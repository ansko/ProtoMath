class Segment:
    """
        A line segment in a 3d space.
    """
    def __init__(self,
                 beg=None, end=None):
        if not None in (beg, end):
            self.beg = beg
            self.end = end


    def dx(self):
        return self.end.x - self.beg.x

    def dy(self):
        return self.end.y - self.beg.y

    def dz(self):
        return self.end.z - self.beg.z

    def length(self):
        return (self.dx**2 + self.dy**2 + self.dz**2)**0.5
