from geometry_primitives_point import Point

# TODO global:
#    inheritance from Polygon

class PolygonRegular:
    """
        A special case of a polygon.
    """
    def __init__(self,
                       vertices=None,
                       center=None, normal=None): # TODO
        if not vertices is None:
            self.init_vertices
        else:
            print('error in regular polygon init:',
                  'incorrect args')
            return None

    def init_vertices(self,
                            vertices):
        self.vertices = vertices
        x = 0
        y = 0
        z = 0
        for pt in self.vertices:
            x += pt.x
            y += pt.y
            z += pt.z
        self.N = len(self.vetices)
        self.center = Point(x / N, y / N, z / N)
        self.outer_radius = None # TODO
        self.inner_radius = None # TODO


    def square(self):       # TODO
        return None

    def perimeter(self):
        return None         # TODO
