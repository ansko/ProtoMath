from linalg_vector import Vector
from linalg_matrix3 import Matrix3


class Line:
    """
        A 1d line in a 3d space.
        Is always set in parametric form:
            x = x0 + tau * dx
            y = y0 + tau * dy
            z = z0 + tau * dz
        where (dx, dy, dz) is the vector parallel to the line
        and (x0, y0, z0) is some chosen point on the line
        (i call it "origin")
    """
    def __init__(self,
                       pt_1=None, pt_2=None,
                       plane_1=None, plane_2=None): # TODO
        if not None in (pt_1, pt_2):
            self.init_2pts(pt_1, pt_2)
        else:
            print('error in line init:',
                  'incorrect args')
            return None

    def init_2pts(self, pt_1, pt_2):
        self.parallel_vector = Vector(pt_2.x - pt_1.x,
                                      pt_2.y - pt_1.y,
                                      pt_2.z - pt_1.z)
        self.origin = pt_1

    def init_2planes(self, plane_1, plane_2):
        pass


    """
        Methods to calculate distances to other primitives.
    """
    def distance_to_point(self, point):
        return point.distance_to_line(self)

    def distance_to_segment(self, segment):
        return segment.distance_to_line(self)

    def distance_to_line(self,
                         line=None,
                         pt_1=None, pt_2=None):
        return self.__implementation_distance_to_line(line=line,
                                                      pt_1=pt_1,
                                                      pt_2=pt_2)

    def __implementation_distance_to_line(self,
                                          line=None,
                                          pt_1=None, pt_2=None):
        """
            Self line AB and line including points C and D. EF is a vector
            perpendicular to segment AB and line CD. E belongs to AB,
            F - to CD. One can write:
                (EF, AB) = 0
                (EF, CD) = 0
                E = A + alpha*AB
                F = C + gamma*CD
            And solve the system finding alpha and gamma.
        """
        ptA = self.origin
        ptB = self.origin.translated(self.parallel_vector)
        if not line is None:
            ptC = line.origin
            ptD = line.origin.translated(line.parallel_vector)
        elif not None in (pt_1, pt_2):
            ptC = pt_1
            ptD = pt_2
        else:
            print('error in line.__implementation_distance_to_line:',
                  'incorrect arguments')
            return None
        vecAB = Vector(pt_1=ptA, pt_2=ptB)
        vecCD = Vector(pt_1=ptC, pt_2=ptD)
        # check if these lines are parallel
        param = abs(vecAB.product_with(vecCD) / vecAB.length() / vecCD.length())
        if param - 1 < 0.001:
            vecAD = Vector(pt_1=ptA, pt_2=ptD)
            cos_angle_A = (vecAD.product_with(vecAB) /
                           vecAB.length() /
                           vecAD.length())
            sin_angle_A = (1 - cos_angle_A**2)**0.5
            return vecAD.length() * sin_angle_A
        # lines are not parallel
        c11 = -vecAB.length()**2
        c12 = vecAB.product_with(vecCD)
        c22 = vecCD.length()**2
        vecBETA = Vector(x=ptC.x - ptA.x, # it is useful
                         y=ptC.y - ptA.y, # to introduce
                         z=ptC.z - ptA.z) # this vector
        b1 = -vecBETA.product_with(vecAB)
        b2 = -vecBETA.product_with(vecCD)
        """
            System to solve is:
            |c11  c12 | b1 |
            |-c12 c22 | b2 |
        """
        print('coeffs: ', c11, c12, c22, b1, b2)
        det = c11*c22 + c12**2
        if det == 0:
            # line and line cross?
            return 0
        det_alpha = b1*c22 - b2*c12
        det_gamma = c11*b2 + c12*b1
        alpha = det_alpha / det
        gamma = det_gamma / det
        vecAB.multiply_by_number(alpha)
        ptE = ptA.translated(vecAB)
        vecCD.multiply_by_number(gamma)
        ptF = ptC.translated(vecCD)
        return Vector(pt_1=ptE, pt_2=ptF).length()

    def distance_to_plane(self,
                          plane=None,
                          pt_1=None, pt_2=None, pt_3=None):
        return self.__implementation_distance_to_plane(plane=plane,
                   pt_1=pt_1, pt_2=pt_2, pt_3=pt_3)

    def __implementation_distance_to_plane(self,
                                           plane=None,
                                           pt_1=None, pt_2=None, pt_3=None):
        """
            Two different ways to check if they are parallel.
            If not, it is easy to find the distance.
        """
        if not plane is None:
            plane_a = plane.a
            plane_b = plane.b
            plane_c = plane.c
            normal = Vector(x=plane_a, y=plane_b, z=plane_c)
            # TODO - remove hardcode
            if abs(self.parallel_vector.product_with(normal)) > 0.001:
                return 0
            return self.origin.distance_to_plane(plane)
        elif not None in (pt_1, pt_2, pt_3):
            x = ((pt_2.y - pt_1.y) * (pt_3.z - pt_1.z) -
                 (pt_3.y - pt_1.y) * (pt_2.z - pt_1.z))
            y = -((pt_2.x - pt_1.x) * (pt_3.z - pt_1.z) -
                  (pt_3.x - pt_1.x) * (pt_2.z - pt_1.z))
            z = ((pt_2.x - pt_1.x) * (pt_3.y - pt_1.y) -
                 (pt_3.x - pt_1.x) * (pt_2.y - pt_1.y))
            normal = Vector(x=x, y=y, z=z)
            # TODO - remove hardcode
            if self.parallel_vector.product_with(normal) > 0.001:
                return 0
            elements = [pt_1.x - self.origin.x,
                        pt_1.y - self.origin.y,
                        pt_1.z - self.origin.z,
                        pt_2.x - self.origin.x,
                        pt_2.y - self.origin.y,
                        pt_2.z - self.origin.z,
                        pt_3.x - self.origin.x,
                        pt_3.y - self.origin.y,
                        pt_3.z - self.origin.z]
            tetrahedron_volume = Matrix3(elements=elements).det() / 6
            vec12 = Vector(pt_1=pt_1, pt_2=pt_2)
            vec13 = Vector(pt_1=pt_1, pt_2=pt_3)
            cos_angle_1 = (vec12.product_with(vec13) /
                           vec12.length() /
                           vec13.length())
            sin_angle_1 = (1 - cos_angle_1**2)**0.5
            triangle_area = vec12.length() * vec13.length() * sin_angle_1 / 2
            return 3 * tetrahedron_volume / triangle_area
        else:
            print('error in line.__implementation_distance_to_plane:',
                  'incorrect arguments')
            return None

    def distance_to_polygon(self,
                            polygon=None,
                            polygon_vertices=None):
        return self.__implementation_distance_to_polygon(polygon,
                                                         polygon_vertices)

    def __implementation_distance_to_polygon(self,
                                             polygon=None,
                                             polygon_vertices=None):
        """
            If the line crosses polygon, return 0. Otherwise,
            the distance of interest equals to the smallest from
            the distances from polygon edges to line.
        """
        if not polygon is None:
            vertices = polygon.vertices
            normal = polygon.containing_plane.normal()
        elif not polygon_vertices is None:
            vertices = polygon_vertices
            dx1 = vertices[1].x - vertices[0].x
            dx2 = vertices[2].x - vertices[0].x
            dy1 = vertices[1].y - vertices[0].y
            dy2 = vertices[2].y - vertices[0].y
            dz1 = vertices[1].z - vertices[0].z
            dz2 = vertices[2].z - vertices[0].z
            normal = Vector(dy1 * dz2 - dz1 * dy2,
                            dx2 * dz1 - dz2 * dx1,
                            dx1 * dy2 - dx2 * dy1)
        else:
            print('error in line.__implementation_distance_to_polygon:',
                  'incorrect arguments')
            return None
        v1 = vertices[0]
        v2 = vertices[1]
        v3 = vertices[2]
        distance_to_plane = self.distance_to_plane(pt_1=v1, pt_2=v2, pt_3=v3)
        if distance_to_plane == 0:
            # There is an intersection.
            # Should find whether this point belongs to the polygon.
            # origin + parallel_vector * alpha = vec01 * gamma + vec02 * beta
            # if 0 < beta, gamma and gamma + beta <= 1
            # intersection point is inside triangle (vertex_0,
            #                                        vertex_i,
            #                                        vertex_i+1)
            # otherwise it 
            x = vertices[0].x
            y = vertices[0].y
            z = vertices[0].z
            dx = self.parallel_vector.x
            dy = self.parallel_vector.y
            dz = self.parallel_vector.z
            smallest_distance = self.distance_to_line(pt_1=vertices[0], # start
                                                      pt_2=vertices[1]) # value
            for i in range(1, len(vertices) - 1):
                vec01 = Vector(pt_1=vertices[0], pt_2=vertices[i])
                vec02 = Vector(pt_1=vertices[0], pt_2=vertices[i + 1])
                det = Matrix3(elements=[dx, -vec01.x, -vec02.x,
                                        dy, -vec02.y, -vec02.y,
                                        dz, -vec02.z, -vec02.z]).det()
                det_alpha = Matrix3(elements=[-x, -vec01.x, -vec02.x,
                                              -y, -vec01.y, -vec02.y,
                                              -z, -vec01.z, -vec02.z]).det()
                det_gamma = Matrix3(elements=[dx, -x, -vec02.x,
                                              dy, -y, -vec02.y,
                                              dz, -z, -vec02.z]).det()
                det_beta = Matrix3(elements=[dx, -vec01.x, -x,
                                             dy, -vec01.y, -y,
                                             dz, -vec01.z, -z]).det()
                # TODO - check this case!
                if det != 0 and (det_gamma != 0 or det_beta != 0):
                    gamma = det_gamma / det
                    beta = det_beta / det
                    if gamma >= 0 and beta >= 0 and gamma + beta <= 1:
                        return 0
                    smallest_distance = min(smallest_distance,
                                            self.distance_to_line(
                                                pt_1=vertices[i],
                                                pt_2=vertices[i + 1]))
                else:
                    # parallel case?
                    smallest_distance = min(smallest_distance,
                                            self.distance_to_point(vertices[i]))
            return smallest_distance
        else:
            # No intersection.
            # Result = (distance_to_plane**2 + in_plane_distance**2)**0.5
            #     in_plane_distance is distance between line and polygon
            #         translated to the line's plane
            normal.renorm(distance_to_plane)
            distances = []
            # distance_in_plane = smallest from distance_to_vertex_in_plane
            for i in range(len(vertices)):
                if i == 0:
                    j = len(vertices) - 1
                else:
                    j = i - 1
                vim1 = vertices[j].translated(normal)
                vim2 = vertices[j].translated(-normal)
                vi1 = vertices[i].translated(normal)
                vi2 = vertices[i].translated(-normal)
                # re-implementation of distance to segment...
                ptC = self.origin
                ptD = self.origin.translated(self.parallel_vector)
                vecCD = Vector(pt_1=ptC, pt_2=ptD)
                for i, vecAB in enumerate((Vector(pt_1=vim1, pt_2=vi1),
                                           Vector(pt_1=vim2, pt_2=vi2))):
                    if i == 0:
                        ptA = vim1
                        ptB = vi1
                    else:
                        ptA = vim2
                        ptB = vi2
                    param = abs(vecAB.product_with(vecCD) /
                                vecAB.length() /
                                vecCD.length())
                    if abs(param - 1) < 0.001:
                        vecAD = Vector(pt_1=ptA, pt_2=ptD)
                        cos_angle_A = (vecAD.product_with(vecAB) /
                                       vecAB.length() /
                                       vecAD.length())
                        sin_angle_A = (1 - cos_angle_A**2)**0.5
                        distances.append(vecAD.length() * sin_angle_A)
                        continue
                    # AB and CD are not parallel
                    c11 = -vecAB.length()**2
                    c12 = vecAB.product_with(vecCD)
                    c22 = vecCD.length()**2
                    vecBETA = Vector(x=self.origin.x - ptA.x, # it is useful
                                     y=self.origin.y - ptA.y, # to introduce
                                     z=self.origin.z - ptA.z) # this vector
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
                        distance_in_plane = 0
                        continue
                    det_alpha = b1*c22 - b2*c12
                    det_gamma = c11*b2 + c12*b1
                    alpha = det_alpha / det
                    gamma = det_gamma / det
                    if alpha <= 0:
                        ptE = ptA
                    elif alpha >=1:
                        ptE = ptB
                    else:
                        vecAB.multiply_by_number(alpha)
                        ptE = self.ptA.translated(vecAB)
                    # gamma may be equal to 0, so use this
                    # instead of Vector.multiply_by_number
                    len_tmp = ((ptE.x - self.origin.x - gamma * vecCD.x)**2 +
                               (ptE.y - self.origin.y - gamma * vecCD.y)**2 +
                               (ptE.z - self.origin.z - gamma * vecCD.z)**2)**0.5
                    distances.append(len_tmp)
            distance_in_plane = min(distances)
            return (distance_in_plane**2 + distance_to_plane**2)**0.5

    def distance_to_prism(self,
                          prism=None,
                          top_facet=None, bot_facet=None):
        return self.__implementation_distance_to_prism(prism, top_facet, bot_facet)

    def __implementation_distance_to_prism(self,
                                           prism,
                                           top_facet, bot_facet):
        if not prism is None:
            top_vertices = prism.top_facet.vertices
            bot_vertices = prism.bot_facet.vertices
        elif not None in (top_facet, bot_facet):
            top_vertices = top_facet.vertices
            bot_vertices = bot_facet.vertices
        else:
            print('error in line.__implementation_distance_to_prism:',
                  'incorrect arguments!')
            return None
        distances = [self.distance_to_polygon(polygon_vertices=top_vertices),
                     self.distance_to_polygon(polygon_vertices=bot_vertices)]
        for i in range(len(top_vertices)):
            # TODO - check that top and bottom vertices correspond
            # one to another
            if i == 0:
                j = len(top_vertices) - 1
            else:
                j = i - 1
            tvi = top_vertices[i]
            tvj = top_vertices[j]
            bvi = bot_vertices[i]
            bvj = bot_vertices[j]
            distance = self.distance_to_polygon(polygon_vertices=[tvi, bvi,
                                                                  bvj, tvj])
            distances.append(distance)
        return min(distances)
