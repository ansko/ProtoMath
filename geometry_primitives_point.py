import math

from linalg_vector import Vector
from linalg_matrix3 import Matrix3
#from geometry_primitives_line import Line
#from geometry_primitives_prism_regular import PrismRegular
#from geometry_primitives_segment import Segment


class Point:
    """
        A point in a 3d space.
    """
    def __init__(self,
                 x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return 'pt(' + str(self.x) + ', ' + str(self.y) + '. ' + str(self.z) + ')'
    def __repr__(self):
        return 'pt(' + str(self.x) + ', ' + str(self.y) + '. ' + str(self.z) + ')'

    """
        A group of methods to get point's properties.
    """
    def from_origin(self):
        """
            Returns the distance from the origin (point with x=y=z=0).
        """
        return (self.x**2 + self.y*2 + self.z**2)**0.5


    """
        Methods to change point.
    """
    def translate(self, vector):
        """
            Translate point to the vector.
        """
        self = self.translated(vector)


    """
        Some useful methods.
    """
    def translated(self, vector):
        """
            Return the result of translation of point to the vector.
        """
        return Point(self.x + vector.x, self.y + vector.y, self.z + vector.z)


    """
        A group of methods to calulate distance to other primitives.
        Other primitives use this methods to calculare the distance to the point.
        If a method returns 0 it means that point belongs to a primitive.
    """
    def distance_to_point(self, pt):
        return self.__implementation_distance_to_point(pt=pt)

    def __implementation_distance_to_point(self,
                                           pt=None,
                                           pt_x=None, pt_y=None, pt_z=None):
        if pt is not None:
           x = pt.x
           y = pt.y
           z = pt.z
        elif not None in (pt_x, pt_y, pt_z):
           x = pt_x
           y = pt_y
           z = pt_z
        else:
           print('error in point __util_distance_to_point:',
                 'incorrect arguments')
           return None
        dx = self.x - x
        dy = self.y - y
        dz = self.z - z
        return (dx**2 + dy**2 + dz**2)**0.5

    def distance_to_line(self, line):
        return self.__implementation_distance_to_line(line=line)

    def __implementation_distance_to_line(self,
                                          line=None,
                                          pt_1=None, pt_2=None,
                                          segment=None):                  # TODO
        """
            pt0, pt1, pt2 form a triangle where
                pt0 = self,
                pt1 = line origin,
                pt2 = line origin + parallel_vector
            Firstly calculate triangle's square as 1/2 * v01 * v02 * sin(a102),
                where a102 is angle between v01 and v02,
                      v01 is vector from pt0 to pt1,
                      v02 is vector from pt0 to pt2.
            Then as 1/2 * h * v12.length()
                where h is height from pt0 to the segment connecting pt1 and pt2
                (the same as line.parallel_vector).
            Equating them one can find h.
        """
        pt0 = self
        if line is not None:
            pt1 = line.origin
            pt2 = pt1.translated(line.parallel_vector)
        elif not None in (pt_1, pt_2):
            pt1 = pt_1
            pt2 = pt_2
        else:
           print('error in point __util_distance_to_line:',
                 'incorrect arguments or not implemented yet')
           return None
        line_parallel_vector_length = pt1.distance_to_point(pt2)
        v01 = Vector(pt_1=pt0, pt_2=pt1)
        v02 = Vector(pt_1=pt0, pt_2=pt2)
        cos_angle_v01_v02 = v01.product_with(v02) / v01.length() / v02.length()
        sin_angle_v01_v02 = (1 - cos_angle_v01_v02**2)**0.5
        double_area = v01.length() * v02.length() * sin_angle_v01_v02
        if double_area == 0:
            return 0
        triangle_height = double_area / line_parallel_vector_length
        return triangle_height

    def distance_to_segment(self, segment):
        return self.__implementation_distance_to_segment(segment=segment)

    def __implementation_distance_to_segment(self,
                                             segment=None,
                                             pt_beg=None, pt_end=None):
        """
            Consider here triangle made by point and segment.
            If there is any angle >= 90 degrees the distance is equal to the length
            of the edge lying near this angle. Otherwise the distance is equal to
            the height of the triangle.
        """
        pt0 = self
        if not segment is None:
            pt1 = segment.pt_1
            pt2 = segment.pt_2
        elif not None in (pt_beg, pt_end):
            pt1 = pt_beg
            pt2 = pt_end
        else:
           print('error in point __util_distance_to_segment:',
                 'incorrect arguments')
           return None
        v01 = Vector(pt_1=pt0, pt_2=pt1)
        v02 = Vector(pt_1=pt0, pt_2=pt2)
        v12 = Vector(pt_1=pt1, pt_2=pt2)
        if v01.product_with(v12) >= 0:
            return v01.length()
        elif v02.product_with(v12) <= 0:
            return v02.length()
        height = self.__implementation_distance_to_line(pt_1=pt1, pt_2=pt2)
        return height

    def distance_to_plane(self,
                          plane=None,
                          pt_1=None, pt_2=None, pt_3=None):
        return self.__implementation_distance_to_plane(plane=plane,
                   pt_1=pt_1, pt_2=pt_2, pt_3=pt_3)

    def __implementation_distance_to_plane(self,
                                           plane=None,
                                           pt_1=None, pt_2=None, pt_3=None): # TODO
        """
             Find plane containing point and parallel to plane.
             Difference in d values is equal to the desired distance.
        """
        if not plane is None:
            plane_a = plane.a
            plane_b = plane.b
            plane_c = plane.c
            plane_d = plane.d
            d = -self.x * plane_a - self.y * plane_b - self.z * plane_c
            return abs(plane_d - d)
        elif not None in (pt_1, pt_2, pt_3):
            pt0 = self
            v01 = Vector(pt_1=pt0, pt_2=pt_1)
            v02 = Vector(pt_1=pt0, pt_2=pt_2)
            v03 = Vector(pt_1=pt0, pt_2=pt_3)
            # TODO - remove hardcode
            if (v01.length() < 0.001 or
                v02.length() < 0.001 or
                v03.length() < 0.001):
                    return 0
            distance_12 = pt_1.distance_to_point(pt_2)
            distance_13 = pt_1.distance_to_point(pt_3)
            distance_23 = pt_2.distance_to_point(pt_3)
            triangle_123_perimeter = distance_12 + distance_13 + distance_23
            matrix_elements = [v01.x, v01.y, v01.z,
                               v02.x, v02.y, v02.z,
                               v03.x, v03.y, v03.z]
            p = triangle_123_perimeter / 2
            triangle_123_area = (p *
                                 (p - distance_12) *
                                 (p - distance_13) *
                                 (p - distance_23)
                                )**0.5
            tetrahedron_volume = abs(Matrix3(elements=matrix_elements).det() / 6)
            tetrahedron_height = tetrahedron_volume * 3 / triangle_123_area
            return tetrahedron_height
        else:
            print('error in __implementation_distance_to_plane:',
                  'incorrect args')
            return None

    def distance_to_polygon_regular(self, polygon):
        return self.distance_to_polygon(polygon)

    def distance_to_polygon(self,
                            polygon=None,
                            polygon_vertices=None):
        return self.__implementation_distance_to_polygon(
                   polygon=polygon,
                   vertices=polygon_vertices)

    def __implementation_distance_to_polygon(self,
                                             polygon=None,
                                             vertices=None):
        """
            Find the distance to the plane containing polygon.
            If it equals zero then desired distance equals to the smallest of
            the distances to the polygon's edges.
            Otherwise, firstly, check whether the desired distance equals to the
            distance to the plane containing poly. It happens if the prism
            with top and bot equal to the poly translated to the vector vec,
            which is perpendicular to poly and has length equal to the distance to
            the plane, contains point.
            Otherwise the distance to the polygon is found by Pythagoras theorem:
            a = the smallest of the diatances to the segments forming prisms's
                top and bottom
            b = distance to the plane containing polygon
            c = (a**2 + b**2)**0.5 - distance of interest
        """
        if not polygon is None:
            distance_to_plane = self.distance_to_plane(
                                    plane=polygon.containing_plane)
            polygon_center_x = polygon.center.x
            polygon_center_y = polygon.center.y
            polygon_center_z = polygon.center.z
            vertex0 = polygon.vertices[0]
            vertex1 = polygon.vertices[1]
            # FIXME - why these coords? they seem to be incorrect!!!
            vec = Vector(x=polygon_center_x - self.x,
                         y=polygon_center_y - self.y,
                         z=polygon_center_z - self.z)
            vertices = polygon.vertices
            top_facet_vertices = [vertex.translated(vec) for vertex in vertices]
            bot_facet_vertices = [vertex.translated(-vec) for vertex in vertices]
        elif not vertices is None and not len(vertices) < 3:
            distance_to_plane = self.__implementation_distance_to_plane(
                pt_1=vertices[0], pt_2=vertices[1], pt_3=vertices[2])
            x = 0
            y = 0
            z = 0
            for vertex in vertices:
                x += vertex.x
                y += vertex.y
                z += vertex.z
            N = len(vertices)
            polygon_center_x = x / N
            polygon_center_y = y / N
            polygon_center_z = z / N
            vertex0 = vertices[0]
            vertex1 = vertices[1]
            vec = Vector(x=polygon_center_x - self.x,
                         y=polygon_center_y - self.y,
                         z=polygon_center_z - self.z)
            top_facet_vertices = [vertex.translated(vec) for vertex in vertices]
            bot_facet_vertices = [vertex.translated(-vec) for vertex in vertices]
        else:
            print('error in point.__implementation_distance_to_polygon:',
                  'incorrect arguments')
            print(polygon, vertices)
            return 0
        # FIXME - remove hardcoded constant
        if distance_to_plane < 0.001:
            impl_d_to_s = self.__implementation_distance_to_segment
            distance = impl_d_to_s(pt_beg=vertices[0], pt_end=vertices[1])
            for i, vertex in enumerate(vertices):
                if i == 0:
                    j = 1
                else:
                    j = i - 1
                distance = min(distance, impl_d_to_s(pt_beg=vertex,
                                                     pt_end=vertices[j])
                              )
            return distance
        if self.__implementation_is_inside_prism(
                top_facet_vertices=top_facet_vertices,
                bot_facet_vertices=bot_facet_vertices):
            return distance_to_plane
        distance_to_segment = self.__implementation_distance_to_segment(
            pt_beg=vertices[0],
            pt_end=vertices[1]) # start value
        for i, vertex in enumerate(vertices):
            if i == 0:
                j = 1
            else:
                j = i - 1
            distance_to_segment = min(distance_to_segment, 
                                      self.__implementation_distance_to_segment(
                                          pt_beg=vertex, 
                                          pt_end=vertices[j]
                                          )
                                      )
        return distance_to_segment


    def distance_to_prism_regular(self, prism):
        return self.distance_to_prism(prism)

    def distance_to_prism(self, prism):
        return self.__implementation_distance_to_prism(prism=prism)

    def __implementation_distance_to_prism(self,
                                           prism=None,
                                           top_facet=None, bot_facet=None):
        """
            If the prism contains point the distance equals zero.
            Otherwise the distance is equal to the smallest of distances
            between point and prism's facets.
        """
        if not prism is None:
            if self.__implementation_is_inside_prism(prism):
                return 0
            top_facet = prism.top_facet
            bot_facet = prism.bot_facet
        elif not None in (top_facet, bot_facet):
            if self.__implementation_is_inside_prism(top_facet=top_facet,
                                                     bot_facet=bot_facet):
                return 0
        else:
            print('error in point.__implementation_distance_to_prism:',
                  'incorrect arguments')
            return None
        # TODO check that top and bottom vertices with same indices correspond
        distance = self.__implementation_distance_to_polygon(polygon=top_facet)
        distance = min(self.__implementation_distance_to_polygon(
                           polygon=bot_facet),
                       distance)
        for i in range(top_facet.N):
            if i == 0:
                j = 1
            else:
                j = i - 1
            vertices = [top_facet.vertices[i],
                        top_facet.vertices[j],
                        bot_facet.vertices[j],
                        bot_facet.vertices[i]]
            distance = min(distance,
                           self.__implementation_distance_to_polygon(
                               vertices=vertices))
        return distance


    """
        Methods to check whether the point is inside other primitive.
    """
    def is_inside_prism(self,
                        prism=None, 
                        top_facet=None, bot_facet=None,
                        top_facet_vertices=None, bot_facet_vertices=None):
       return self.__implementation_is_inside_prism(prism=prism,
                          top_facet=top_facet, bot_facet=bot_facet, 
                          top_facet_vertices=top_facet_vertices,
                          bot_facet_vertices=bot_facet_vertices)

    def __implementation_is_inside_prism(self,
            prism=None,
            top_facet=None, bot_facet=None,
            top_facet_vertices=None, bot_facet_vertices=None): # TODO
       """
           Check whether the point is inside of a given prism.
           If the sum of the distances from the point to the top and bottom
           facets does not equal to the prism height, the point is not located
           between the planes containing top and bottom facets
           consequently it is not inside the prism.
           After that if the volume of the prism equals to the sum of volumes
           of pyramides formed by prism's facets and point, the point is inside.
           In other case it is not.
       """
       if not prism is None:
           top_facet = prism.top_facet
           bot_facet = prism.bot_facet
           facet_area = top_facet.square()
           facet_edge_length = top_facet.edge_length
           height = prism.height
           top_plane = top_facet.containing_plane
           bot_plane = bot_facet.containing_plane
           distance_top_plane = self.distance_to_plane(plane=top_plane)
           distance_bot_plane = self.distance_to_plane(plane=bot_plane)
           if abs(distance_top_plane + distance_bot_plane - height) > 0.001:
               return False
           volume_prism = height * facet_area
           # pyramides made by top and bottom facets and center of the prism
           volume_pyramides = 2/3 * facet_area * height
           # pyramides made by side facets and center of the prism
           area_side_facet = height * facet_edge_length
           for i in range(len(top_facet.vertices)):
               if i == 0:
                    j = 1
               else:
                    j = i - 1
               height_to_side = self.__implementation_distance_to_plane(
                   pt_1=top_facet.vertices[i],
                   pt_2=top_facet.vertices[j],
                   pt_3=bot_facet.vertices[j]
               )
               volume_side_pyramide = 1/3 * area_side_facet * height_to_side
               volume_pyramides += volume_side_pyramide
           # FIXME - remove hardcoded constant
           if abs(volume_pyramides - volume_prism) < 0.001:
               return True
       elif not None in (top_facet, bot_facet):
           # TODO this way: height = top_facet.distance_to_polygon(bot_facet)
           height = top_facet.center.distance_to_point(bot_facet.center)
           facet_area = top_facet.square()
           facet_edge_length = top_facet.edge_length
           top_plane = top_facet.containing_plane
           bot_plane = bot_facet.containing_plane
           distance_top_plane = self.distance_to_plane(plane=top_plane)
           distance_bot_plane = self.distance_to_plane(plane=bot_plane)
           # FIXME - remove hardcoded constant
           if abs(distance_top_plane + distance_bot_plane - height) > 0.001:
               return False
           volume_prism = height * facet_area
           # pyramides made by top and bottom facets and center of the prism
           volume_pyramides = 2/3 * facet_area * height
           # pyramides made by side facets and center of the prism
           area_side_facet = height * facet_edge_length
           for i in range(len(top_facet.vertices)):
               if i == 0:
                    j = 1
               else:
                    j = i - 1
               height_to_side = self.__implementation_distance_to_plane(
                   pt_1=top_facet.vertices[i],
                   pt_2=top_facet.vertices[j],
                   pt_3=bot_facet.vertices[j]
               )
               volume_side_pyramide = 1/3 * area_side_facet * height_to_side
               volume_pyramides += volume_side_pyramide
           # FIXME - remove hardcoded constant
           if abs(volume_pyramides - volume_prism) < 0.001:
               return True
       elif not None in (top_facet_vertices, bot_facet_vertices):
           # TODO check that top and bottom correspond
           height = top_facet_vertices[0].distance_to_point(
                        bot_facet_vertices[0])
           # find top facet center
           x = 0
           y = 0
           z = 0
           for vertex in top_facet_vertices:
               x += vertex.x
               y += vertex.y
               z += vertex.z
           N = len(top_facet_vertices)
           x /= N 
           y /= N
           z /= N
           # find area of top and bottom
           dx = top_facet_vertices[0].x - x
           dy = top_facet_vertices[0].y - y
           dz = top_facet_vertices[0].z - z
           outer_radius = (dx**2 + dy**2 + dz**2)**0.5
           inner_radius = outer_radius * math.sin(math.pi / N)
           facet_edge_length = top_facet_vertices[0].distance_to_point(
               top_facet_vertices[1])
           triangle_area = 0.5 * inner_radius * facet_edge_length
           facet_area = N * triangle_area
           # check whether volumes are equal
           volume_prism = height * facet_area
           volume_pyramides = 1/3 * facet_area * height # top and bot
           area_side_facet = height * facet_edge_length
           #volume_pyramides = 0
           for i in range(len(top_facet_vertices)):
               if i == 0:
                    j = 1
               else:
                    j = i - 1
               height_to_side = self.__implementation_distance_to_plane(
                   pt_1=top_facet_vertices[i],
                   pt_2=top_facet_vertices[j],
                   pt_3=bot_facet_vertices[j]
               )
               #print('pts ', self,
               #              top_facet_vertices[i],
               #              top_facet_vertices[j],
               #              bot_facet_vertices[j])
               volume_side_pyramide = 1/3 * area_side_facet * height_to_side
               volume_pyramides += volume_side_pyramide
           if abs(volume_pyramides - volume_prism) < 0.001:
               return True
       else:
           print('error in __implementation_is_inside_prism:',
                 'incorrect args')
           return None
       return False
