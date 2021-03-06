from linalg_vector import Vector


class Plane:
    """
        A 2d plane in a 3d space.
        Has a lot of init methods.
        A plane is always set as ax + by + cz + d = 0
    """
    def __init__(self,
                 a=None, b=None, c=None, d=None,
                 pt_1=None, pt_2=None, pt_3=None,
                 pt=None, normal=None,
                          segment=None,
                          line=None,              # TODO
                 segment_1=None, segment_2=None): # TODO
        if not None in (a, b, c, d):
            self.init_equation(a, b, c, d)
        elif not None in (pt_1, pt_2, pt_3):
            self.init_3pts(pt_1, pt_2, pt_3)
        elif not None in (pt, normal):
            self.init_pt_normal(pt, normal)
        elif not None in (pt, segment):
            self.init_pt_segment(pt, segment)
        else:
            print('error in plane init:',
                  'incorrect args')
            return None

    def init_equation(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def init_3pts(self,
                  pt_1, pt_2, pt_3):
        """
            Knowing coordinates of three pts we can find equation as
            | x  - x1   y  - y1   z  - z1 |
            | x2 - x1   y2 - y1   z2 - z1 | = 0
            | x3 - x1   y3 - y1   z3 - z1 |
        """
        # check wether these pts are not at one line
        distance_12 = ((pt_2.x - pt_1.x)**2 +
                       (pt_2.y - pt_1.y)**2 +
                       (pt_2.z - pt_1.z)**2)**0.5
        distance_13 = ((pt_3.x - pt_1.x)**2 +
                       (pt_3.y - pt_1.y)**2 +
                       (pt_3.z - pt_1.z)**2)**0.5
        distance_23 = ((pt_3.x - pt_2.x)**2 +
                       (pt_3.y - pt_2.y)**2 +
                       (pt_3.z - pt_2.z)**2)**0.5
            # Cauchy–Bunyakovsky–Schwarz inequality
        if (distance_12 + distance_13 <= distance_23 or
            distance_12 + distance_23 <= distance_13 or
            distance_13 + distance_23 <= distance_12):
                print('error in plane init:',
                      'points do not determine a plane')
                return None
        # find equation
        minor_x = ((pt_2.y - pt_1.y) * (pt_3.z - pt_1.z) -
                   (pt_3.y - pt_1.y) * (pt_2.z - pt_1.z))
        minor_y = ((pt_3.x - pt_1.x) * (pt_2.z - pt_1.z) -
                   (pt_2.x - pt_1.x) * (pt_3.z - pt_1.z))
        minor_z = ((pt_2.x - pt_1.x) * (pt_3.y - pt_1.y) -
                   (pt_2.y - pt_1.y) * (pt_3.x - pt_1.x))
            # incorrect case when all minors are equal to zero
        if minor_x ==0 and minor_y == 0 and minor_z == 0:
            print('error in plane init:',
                  'all minors in init_3pts are equal to zero')
            return None
            # if some_minor == 0 than
            # the plane is parallel to some axis or plane (i.e. 0xy)
                # two minors are zero
        if minor_x == 0 and minor_y == 0:
            self.a = 0
            self.b = 0
            self.c = 1
            self.d = -pt_1.z
        elif minor_x == 0 and minor_z == 0:
            self.a = 0
            self.b = 1
            self.c = 0
            self.d = -pt_1.y
        elif minor_y == 0 and minor_z == 0:
            self.a = 1
            self.b = 0
            self.c = 0
            self.d = -pt_1.x
                 # just one minor is zero
        elif minor_x == 0:
            self.a = 0
            self.b = 1
            self.c = minor_z / minor_y
            self.d = -pt_1.y - minor_z/minor_y*pt_1.z
        elif minor_y == 0:
            self.a = 1
            self.b = 0
            self.c = minor_z / minor_x
            self.d = -pt_1.x - minor_z/minor_x*pt_1.z
        elif minor_z == 0:
            self.a = 1
            self.b = minor_y / minor_x
            self.c = 0
            self.d = -pt_1.x - minor_y/minor_x*pt_1.y
                 # there is not minor equal to zero
        else:
            self.a = 1
            self.b = minor_y / minor_x
            self.c = minor_z = minor_x
            self.d = -pt_1.x - minor_y/minor_x*pt_1.y - minor_z/minor_x*pt_1.z

    def init_pt_normal(self, pt, normal):
        self.a = normal.x
        self.b = normal.y
        self.c = normal.z
        self.d = -pt.x*self.a - pt.y*self.b - pt.z*self.c

    def init_pt_segment(self, pt, segment):
        self.init_3pts(pt, segment.beg, segment.end)


    """
        Some properties of the defined plane.
    """
    def normal(self):
        """
            Return normal to the plane.
        """
        return Vector(self.a, self.b, self.c)

    def get_semispace(self, pt):
        """
            The sign of the return value defines the semispace
            where does defined point lie. It is useful from the
            understanding whether some segment crosses the plane.
            (if does, the return values for its ends will have
            different signs).
        """
        return self.a * pt.x + self.b * pt.y + self.c * pt.z + self.d


    """
        Methods to calculate distances to other primitives.
    """
    def distance_to_point(self, point):
        return point.distance_to_plane(self)

    def distance_to_line(self, line):
        return line.distance_to_plane(self)

    def distance_to_segment(self, segment):
        return segment.distance_to_plane(self)

    def distance_to_plane(self, plane):
        normal = self.normal()
        other_normal = plane.normal()
        cos_angle = (normal.product_with(other_normal) /
                     normal.length() /
                     other_normal.length())
        # TODO - remove hardcode
        if abs(abs(cos_angle) - 1) < 0.001:
            return abs(self.d - plane.d)
        return 0

    def distance_to_polygon(self, polygon):
        signum0 = self.get_semispace(polygon.vertices[0])
        for i in range(1, len(polygon.vertices)):
            if signum0 * self.get_semispace(polygon.vertices[i]) < 0:
                return 0
        return min([vertex.distance_to_plane(self) for vertex in polygon.vertices])

    def distance_to_prism(self, prism):
        signum0 = self.get_semispace(prism.top_facet.vertices[0])
        for poly in (prism.top_facet, prism.bot_facet):
            for vertex in poly.vertices:
                if signum0 * self.get_semispace(vertex) < 0:
                    return 0
        return min(self.distance_to_polygon(prism.top_facet),
                   self.distance_to_polygon(prism.bot_facet))
