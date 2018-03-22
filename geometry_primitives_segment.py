from linalg_vector import Vector
from linalg_matrix3 import Matrix3


class Segment:
    """
        A line segment in a 3d space.
    """
    def __init__(self,
                 pt_1=None, pt_2=None):
        if not None in (pt_1, pt_2):
            self.pt_1 = pt_1
            self.pt_2 = pt_2


    def dx(self):
        return self.pt_2.x - self.pt_1.x

    def dy(self):
        return self.pt_2.y - self.pt_1.y

    def dz(self):
        return self.pt_2.z - self.pt_1.z

    def length(self):
        return (self.dx**2 + self.dy**2 + self.dz**2)**0.5


    """
        A group of methods to calculate distances to other primitives.
    """
    def distance_to_point(self, point):
        return point.distance_to_segment(self)

    def distance_to_line(self, line):
        return self.__implementation_distance_to_line(line=line)

    def __implementation_distance_to_line(self,
                                          line=None,
                                          pt_1=None, pt_2=None):
        """
            Segment AB and line including points C and D. EF is a vector
            perpendicular to segment AB and line CD. E belongs to AB,
            F - to CD. One can write:
                (EF, AB) = 0
                (EF, CD) = 0
                E = A + alpha*AB
                F = C + gamma*CD
            And solve the system finding alpha and gamma.
            If 0 <= alpha <= 1, desired distance equals
            to the length of EF. Otherwise it equals to the less
            of the distances from segment's point to line.
        """
        vecAB = Vector(segment=self)
        if line is not None:
            vecCD = Vector(pt_1=line.origin,
                           pt_2=line.origin.translated(line.parallel_vector))
            ptD = pt_2=line.origin.translated(line.parallel_vector)
            line_origin_x = line.origin.x
            line_origin_y = line.origin.y
            line_origin_z = line.origin.z
        elif not None in (pt_1, pt_2):
            vecCD = Vector(pt_1=pt_1, pt_2=pt_2)
            line_origin_x = pt_1.x
            line_origin_y = pt_1.y
            line_origin_z = pt_1.z
            ptD = pt_2
        # check if line and segment are parallel
        param = abs(vecAB.product_with(vecCD) / vecAB.length() / vecCD.length())
        if abs(param - 1) < 0.001:
            vecAD = Vector(pt_1=self.pt_1, pt_2=ptD)
            cos_angle_A = (vecAD.product_with(vecAB) /
                           vecAB.length() /
                           vecAD.length())
            sin_angle_A = (1 - cos_angle_A**2)**0.5
            return vecAD.length() * sin_angle_A
        # lines are not parallel
        c11 = -vecAB.length()**2
        c12 = vecAB.product_with(vecCD)
        c22 = vecCD.length()**2
        vecBETA = Vector(x=line_origin_x - self.pt_1.x, # it is useful
                         y=line_origin_y - self.pt_1.y, # to introduce
                         z=line_origin_z - self.pt_1.z) # this vector
        b1 = -vecBETA.product_with(vecAB)
        b2 = -vecBETA.product_with(vecCD)
        """
            System to solve is:
            |c11  c12 | b1 |
            |-c12 c22 | b2 |
        """
        det = c11*c22 + c12**2
        if det == 0:
            # segment and line cross?
            return 0
        det_alpha = b1*c22 - b2*c12
        det_gamma = c11*b2 + c12*b1
        alpha = det_alpha / det
        gamma = det_gamma / det
        if alpha <= 0:
            ptE = self.pt_1
        elif alpha >=1:
            ptE = self.pt_2
        else:
            vecAB.multiply_by_number(alpha)
            ptE = self.pt_1.translated(vecAB)
        vecCD.multiply_by_number(gamma)
        ptF = line.origin.translated(vecCD)
        return Vector(pt_1=ptE, pt_2=ptF).length()

    def distance_to_segment(self, segment):
        return self.__implementation_distance_to_segment(segment=segment)

    def __implementation_distance_to_segment(self,
                                             segment=None,
                                             pt_1=None, pt_2=None):
        """
            Almost the same as distance to line, but not only
            should be 0 <= alpha <= 1, also 0 <= gamma <= 1
        """
        if not segment is None:
             pt1 = segment.pt_1
             pt2 = segment.pt_2
        elif not None in (pt_1, pt_2):
             pt1 = pt_1
             pt2 = pt_2
        vecAB = Vector(segment=self)
        vecCD = Vector(pt_1=pt1, pt_2=pt2)
        # check if segments are parallel!
        par = abs(vecAB.product_with(vecCD) / vecAB.length() / vecCD.length()) - 1
        # TODO -remove hardcode
        if abs(par) <= 0.001:
            vecAD = Vector(pt_1=pt1, pt_2=self.pt_2)
            cos_angleA = abs(vecAB.product_with(vecAD) /
                                 vecAB.length() /
                                 vecAD.length())
            sin_angleA = (1 - cos_angleA**2)**0.5
            return vecAD.length() * sin_angleA
        c11 = -vecAB.length()**2
        c12 = vecAB.product_with(vecCD)
        c22 = vecCD.length()**2
        vecBETA = Vector(x=pt1.x - self.pt_1.x, # it is useful
                         y=pt1.y - self.pt_1.y, # to introduce
                         z=pt1.z - self.pt_1.z) # this vector
        b1 = -vecBETA.product_with(vecAB)
        b2 = -vecBETA.product_with(vecCD)
        """
            System to solve is:
            |  c11   c12  |  b1  |
            | -c12   c22  |  b2  |
        """
        det = c11*c22 + c12**2
        if det == 0:
            # segment and segment cross?
            return 0
        det_alpha = b1*c22 - b2*c12
        det_gamma = c11*b2 + c12*b1
        alpha = det_alpha / det
        gamma = det_gamma / det
        if alpha <= 0:
            ptE = self.pt_1
        elif alpha >= 1:
            ptE = self.pt_2
        else:
            vecAB.multiply_by_number(alpha)
            ptE = self.pt_1.translated(vecAB)
        if gamma <= 0:
            ptF = pt1
        elif gamma >= 1:
            ptF = pt2
        else:
            vecCD.multiply_by_number(gamma)
            ptF = pt1.translated(vecCD)
        return Vector(pt_1=ptE, pt_2=ptF).length()

    def distance_to_plane(self, plane):
        return self.__implementation_distance_to_plane(plane=plane)

    def __implementation_distance_to_plane(self,
                                           plane=None,
                                           pt_1=None, pt_2=None, pt_3=None):
        """
            If plane and segment do not intersect, distance equals
            to the smallest between the distances from segment's ends
            to plane.
        """
        if not plane is None:
            sign1 = plane.get_semispace(self.pt_1)
            sign2 = plane.get_semispace(self.pt_2)
            if sign1 * sign2 <= 0:                    # segment and plane cross
               return 0
            return min(self.pt_1.distance_to_plane(plane),
                       self.pt_2.distance_to_plane(plane))
        elif not None in (pt_1, pt_2, pt_3):
            elements1 = [pt_1.x - self.pt_1.x,
                         pt_1.y - self.pt_1.y,
                         pt_1.z - self.pt_1.z,
                         pt_2.x - self.pt_1.x,
                         pt_2.y - self.pt_1.y,
                         pt_2.z - self.pt_1.z,
                         pt_3.x - self.pt_1.x,
                         pt_3.y - self.pt_1.y,
                         pt_3.z - self.pt_1.z]
            elements2 = [pt_1.x - self.pt_2.x,
                         pt_1.y - self.pt_2.y,
                         pt_1.z - self.pt_2.z,
                         pt_2.x - self.pt_2.x,
                         pt_2.y - self.pt_2.y,
                         pt_2.z - self.pt_2.z,
                         pt_3.x - self.pt_2.x,
                         pt_3.y - self.pt_2.y,
                         pt_3.z - self.pt_2.z]
            sign1 = Matrix3(elements=elements1).det()
            sign2 = Matrix3(elements=elements2).det()
            if sign1 * sign2 <= 0:
               return 0
            v12 = Vector(pt_1=pt_1, pt_2=pt_2)
            v13 = Vector(pt_1=pt_1, pt_2=pt_3)
            v23 = Vector(pt_1=pt_2, pt_2=pt_3)
            cos_angle_1 = v12.product_with(v13) / v12.length() / v13.length()
            sin_angle_1 = (1 - cos_angle_1**2)**0.5
            triangle_square = 0.5 * v12.length() * v13.length() * sin_angle_1
            return 3 * min(abs(sign1), abs(sign2)) / triangle_square

    def distance_to_polygon(self,
                            polygon=None,
                            polygon_vertices=None):
        return self.__implementation_distance_to_polygon(polygon,
                                                         polygon_vertices)

    def __implementation_distance_to_polygon(self,
                                             polygon=None,
                                             polygon_vertices=None): # TODO
        """
            1) Does segment cross plane where does poly lie?
             2a) If does, does the intersection point belong to poly?
              2aa) If yes - return 0.
              2ab) If not - return the smallest from the distances to
                   the polygon's edges.
             2b) If not - does the closest segment's end to the plane
                 lie in the prism?
              2ba) If yes - return distance to the plane.
              2bb) If not - return the less from the distances to
                   the polygon's edges.
        """
        if polygon is not None:
            polygon_vertices = polygon.vertices
            plane_pt_1 = polygon.vertices[0]
            plane_pt_2 = polygon.vertices[1]
            plane_pt_3 = polygon.vertices[2]
            normal_to_plane = Vector(x=polygon.containing_plane.a,
                                     y=polygon.containing_plane.b,
                                     z=polygon.containing_plane.c)
        else:
            plane_pt_1 = polygon_vertices[0]
            plane_pt_2 = polygon_vertices[1]
            plane_pt_3 = polygon_vertices[2]
            x = ((plane_pt_2.y - plane_pt_1.y) * (plane_pt_3.z - plane_pt_1.z) -
                 (plane_pt_3.y - plane_pt_1.y) * (plane_pt_2.z - plane_pt_1.z))
            y = (-(plane_pt_2.x - plane_pt_1.x) * (plane_pt_3.z - plane_pt_1.z) +
                  (plane_pt_3.x - plane_pt_1.x) * (plane_pt_2.z - plane_pt_1.z))
            z = ((plane_pt_2.x - plane_pt_1.x) * (plane_pt_3.y - plane_pt_1.y) -
                 (plane_pt_3.x - plane_pt_1.x) * (plane_pt_2.y - plane_pt_1.y))
            normal_to_plane = Vector(x=x, y=y, z=z)
        distance_to_plane = self.__implementation_distance_to_plane(
                                pt_1=plane_pt_1,
                                pt_2=plane_pt_2,
                                pt_3=plane_pt_3)
        if distance_to_plane <= 0.001:
            dist1 = self.pt_1.distance_to_plane(pt_1=plane_pt_1,
                                                pt_2=plane_pt_2,
                                                pt_3=plane_pt_3)
            dist2 = self.pt_2.distance_to_plane(pt_1=plane_pt_1,
                                                pt_2=plane_pt_2,
                                                pt_3=plane_pt_3)
            if dist1 <= 0.001:
                intersection_point = self.pt_1
            elif dist2 <= 0.001:
                intersection_point = self.pt_2
            else:
                v12 = Vector(segment=self)
                v12.multiply_by_number(dist1 / (abs(dist1) + abs(dist2)))
                intersection_point = self.pt_1.translated(v12)
            if intersection_point.distance_to_polygon(
                   polygon_vertices=polygon_vertices) == 0:
                return 0
            distance = self.distance_to_segment(Segment(pt_1=polygon_vertices[0],
                                                        pt_2=polygon_vertices[1]))
            for i, vertex in enumerate(polygon_vertices):
                if i == 0:
                    j = 1
                else:
                    j = i - 1
                vertex1 = polygon_vertices[j]
                distance1 = self.distance_to_segment(Segment(pt_1=vertex,
                                                             pt_2=vertex1))
                distance = min(distance, distance1)
            return distance
        # distance_to_plane != 0
        dist1 = self.pt_1.distance_to_plane(pt_1=plane_pt_1,
                                            pt_2=plane_pt_2,
                                            pt_3=plane_pt_3)
        dist2 = self.pt_2.distance_to_plane(pt_1=plane_pt_1,
                                            pt_2=plane_pt_2,
                                            pt_3=plane_pt_3)
        if dist1 <= dist2:
            normal = normal_to_plane
            normal.renorm(dist1)
            # TODO
            if not polygon is None:
                top_facet_vertices = polygon.translated(normal).vertices
                bot_facet_vertices = polygon.translated(-normal).vertices
            elif not polygon_vertices is None:
                top_facet_vertices = [vertex.translated(normal)
                    for vertex in polygon_vertices]
                bot_facet_vertices = [vertex.translated(-normal)
                    for vertex in polygon_vertices]
            if self.pt_1.is_inside_prism(
                   top_facet_vertices=top_facet_vertices,
                   bot_facet_vertices=bot_facet_vertices):
                return dist1
            else:
                distance = self.distance_to_segment(
                                   Segment(pt_1=polygon_vertices[0],
                                           pt_2=polygon_vertices[1]))
                for i, vertex in enumerate(polygon_vertices):
                    if i == 0:
                        j = 1
                    else:
                        j = i - 1
                    vertex1 = polygon_vertices[j]
                    distance1 = self.distance_to_segment(Segment(pt_1=vertex,
                                                                 pt_2=vertex1))
                    distance = min(distance, distance1)
                return distance
        else:
            normal = normal_to_plane
            normal.renorm(dist2)
            if self.pt_2.is_inside_prism(
                   top_facet_vertices=top_facet_vertices,
                   bot_facet_vertices=bot_facet_vertices):
                return dist2
            else:
                distance = self.distance_to_segment(
                                   Segment(pt_1=polygon_vertices[0],
                                           pt_2=polygon_vertices[1]))
                for i, vertex in enumerate(polygon_vertices):
                    if i == 0:
                        j = 1
                    else:
                        j = i - 1
                    vertex1 = polygon.vertices[j]
                    distance1 = self.distance_to_segment(Segment(pt_1=vertex,
                                                                 pt_2=vertex1))
                    distance = min(distance, distance1)
                return distance

    def distance_to_prism(self, prism):
        """
            If any of segment's ends belong to prism return 0.
            Otherwise return minimal from the distances to prism's facets.
        """
        if self.pt_1.is_inside_prism(prism):
            return 0
        if self.pt_2.is_inside_prism(prism):
            return 0
        top_facet = prism.top_facet
        bot_facet = prism.bot_facet
        distance = self.distance_to_polygon(polygon=top_facet)
        distance = min(distance, self.distance_to_polygon(polygon=bot_facet))
        for i in range(len(top_facet.vertices)):
            if i == 0:
                j = 1
            else:
                j = i - 1
            v1 = top_facet.vertices[i]
            v2 = top_facet.vertices[j]
            v3 = bot_facet.vertices[j]
            v4 = bot_facet.vertices[i]

            distance = min(distance,
                           self.distance_to_polygon(
                               polygon_vertices=[v1, v2, v3, v4]))
        return distance
