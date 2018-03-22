#!/usr/bin/env python3


from geometry_primitives_line import Line
from geometry_primitives_plane import Plane
from geometry_primitives_point import Point
from geometry_primitives_polygon_regular import PolygonRegular
from geometry_primitives_prism_regular import PrismRegular
from geometry_primitives_segment import Segment

from linalg_matrix2 import Matrix2
from linalg_matrix3 import Matrix3
from linalg_matrix4 import Matrix4
from linalg_vector import Vector


def test_distance_point():
    print('plane-pt')
    pt = Point(0, 0, 0)
    pt1 = Point(0, 0, 1)
    pt2 = Point(1, 0, 1)
    pt3 = Point(1, 1, 1)
    plane = Plane(pt_1=pt1, pt_2=pt2, pt_3=pt3)
    print(plane.distance_to_point(pt))

def test_distance_line():
    print('plane-line')
    pt1 = Point(0, 0, 1)
    pt2 = Point(1, 0, 1)
    pt3 = Point(1, 1, 1)
    pt4 = Point(0, 0, 0)
    pt5 = Point(1, 1, 0)
    pt6 = Point(0, 1, 1)
    line1 = Line(pt_1=pt4, pt_2=pt5)
    line2 = Line(pt_1=pt4, pt_2=pt6)
    plane = Plane(pt_1=pt1, pt_2=pt2, pt_3=pt3)
    print(plane.distance_to_line(line1)) # should be 1
    print(plane.distance_to_line(line2)) # they intersect

def test_distance_segment():
    print('plane-seg')
    pt1 = Point(0, 0, 1)
    pt2 = Point(1, 0, 1)
    pt3 = Point(1, 1, 1)
    pt4 = Point(0, 0, 0)
    pt5 = Point(1, 1, 0)
    pt6 = Point(0, 0, 2)
    seg1 = Segment(pt_1=pt4, pt_2=pt5)
    seg2 = Segment(pt_1=pt4, pt_2=pt6)
    plane = Plane(pt_1=pt1, pt_2=pt2, pt_3=pt3)
    print(plane.distance_to_segment(seg1)) # should be 1
    print(plane.distance_to_segment(seg2)) # they intersect

def test_distance_plane():
    print('plane-plane')
    pt1 = Point(0, 0, 1)
    pt2 = Point(1, 0, 1)
    pt3 = Point(1, 1, 1)
    pt4 = Point(0, 0, 3)
    pt5 = Point(1, 0, 3)
    pt6 = Point(1, 1, 3)
    pt7 = Point(0, 0, 2)
    pt8 = Point(1, 0, 3)
    pt9 = Point(1, 1, 3)
    plane1 = Plane(pt_1=pt1, pt_2=pt2, pt_3=pt3)
    plane2 = Plane(pt_1=pt4, pt_2=pt5, pt_3=pt6)
    plane3 = Plane(pt_1=pt7, pt_2=pt8, pt_3=pt9)
    print(plane1.distance_to_plane(plane2)) # should be 2
    print(plane1.distance_to_plane(plane3)) # they intersect

def test_distance_polygon():
    print('plane-poly')
    pt1 = Point(0, 0, 1)
    pt2 = Point(1, 0, 1)
    pt3 = Point(1, 1, 1)
    pt4 = Point(0, 0, 3)
    pt5 = Point(1, 0, 3)
    pt6 = Point(1, 1, 3)
    pt7 = Point(0, 0, -3)
    pt8 = Point(1, 0, 3)
    pt9 = Point(1, 1, 3)
    plane = Plane(pt_1=pt1, pt_2=pt2, pt_3=pt3)
    poly1 = PolygonRegular(vertices=[pt4, pt5, pt6])
    poly2 = PolygonRegular(vertices=[pt7, pt8, pt9])
    print(plane.distance_to_polygon(poly1)) # should be 2
    print(plane.distance_to_polygon(poly2)) # they intersect

def test_distance_prism():
    print('plane-prism')
    pt1 = Point(0, 0, 1)
    pt2 = Point(1, 0, 1)
    pt3 = Point(1, 1, 1)
    pt4 = Point(0, 0, 3)
    pt5 = Point(1, 0, 3)
    pt6 = Point(1, 1, 3)
    pt7 = Point(0, 0, -3)
    pt8 = Point(1, 0, -3)
    pt9 = Point(1, 1, -3)
    pt10 = Point(0, 0, 5)
    pt11 = Point(0, 1, 5)
    pt12 = Point(1, 1, 5)
    plane = Plane(pt_1=pt1, pt_2=pt2, pt_3=pt3)
    top_facet = PolygonRegular(vertices=[pt4, pt5, pt6])
    bot_facet = PolygonRegular(vertices=[pt7, pt8, pt9])
    bot_facet2 = PolygonRegular(vertices=[pt10, pt11, pt12])
    prism1 = PrismRegular(top_facet, bot_facet)
    prism2 = PrismRegular(top_facet, bot_facet2)
    print(plane.distance_to_prism(prism1)) # they intersect
    print(plane.distance_to_prism(prism2)) # should be 2


def test_distances():
    print('start testing distances from plane to others...\n')
    test_distance_point()
    test_distance_line()
    test_distance_segment()
    test_distance_plane()
    test_distance_polygon()
    test_distance_prism()
    print('\nfinished')


test_distances()
