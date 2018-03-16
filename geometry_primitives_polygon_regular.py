import math

from geometry_primitives_plane import Plane
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
            self.init_vertices(vertices)
        else:
            print('error in regular polygon init:',
                  'incorrect args')
            return None

    def init_vertices(self,
                            vertices):
        if len(vertices) < 3:
            print('error in poly init_vertices:',
                  'not enough vertices number')
            return None
        self.vertices = vertices
        x = 0
        y = 0
        z = 0
        for pt in self.vertices:
            x += pt.x
            y += pt.y
            z += pt.z
        self.N = len(self.vertices)
        self.central_angle = math.pi / self.N
        # TODO: center is useful, but imports are recursive if uncomment next line
        self.center = Point(x / self.N, y / self.N, z / self.N)
        self.edge_length = self.vertices[-1].distance_to_point(self.vertices[0])
        self.outer_radius = self.edge_length / 2 / math.sin(self.central_angle)
        self.inner_radius = (self.outer_radius**2 - self.edge_length**2 / 4)**0.5
        self.containing_plane = Plane(pt_1=self.vertices[0],
                                      pt_2=self.vertices[1],
                                      pt_3=self.vertices[2])

    """
        A group of methods to get poly's properties.
    """
    def square(self):
        return self.N * self.edge_length * self.inner_radius / 2

    def perimeter(self):
        return self.N * self.edge_length

    """
        Methods to change poly's properties.
    """
    def translate(self, vector):
        self = self.translated(vector)

    # TODO rotation?
    # TODO change by matrix?

    """
        Some useful methods.
    """
    def translated(self, vector):
        translated_vertices = []
        for vertex in self.vertices:
            translated_vertices.append(vertex.translated(vector))
        return PolygonRegular(vertices=translated_vertices)
