class Point:
    """
        A point in a 3d space.
    """
    def __init__(self,
                 x, y, z):
        self.x = x
        self.y = y
        self.z = z


    def from_origin(self):
        """
            Returns the distance from the origin.
        """
        return (self.x**2 + self.y*2 + self.z**2)**0.5
