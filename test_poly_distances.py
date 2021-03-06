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
    print('poly-pt')
    pt = Point(0, 0, 0)
    pt1 = Point(0, 1, 1)
    pt2 = Point(0, 0, 1)
    pt3 = Point(1, 0, 1)
    pt4 = Point(1, 1, 1)
    poly = PolygonRegular(vertices=[pt1, pt2, pt3, pt4])
    print(poly.distance_to_point(pt)) # should be 1

def test_distance_line():
    print('poly-line')
    pt1 = Point(0, 1, 1)
    pt2 = Point(0, 0, 1)
    pt3 = Point(1, 0, 1)
    pt4 = Point(1, 1, 1)
    pt5 = Point(0, 0, 2)
    pt6 = Point(0, 1, 2)
    pt7 = Point(0, 0, 3)
    poly = PolygonRegular(vertices=[pt1, pt2, pt3, pt4])
    line1 = Line(pt_1=pt5, pt_2=pt6)
    line2 = Line(pt_1=pt5, pt_2=pt7)
    print(poly.distance_to_line(line1)) # should be 1
    print(poly.distance_to_line(line2)) # they intersect

def test_distance_segment():
    print('poly-seg')
    pt1 = Point(0, 1, 1)
    pt2 = Point(0, 0, 1)
    pt3 = Point(1, 0, 1)
    pt4 = Point(1, 1, 1)
    pt5 = Point(0, 0, 2)
    pt6 = Point(0, 1, 2)
    pt7 = Point(0, 0, -2)
    poly = PolygonRegular(vertices=[pt1, pt2, pt3, pt4])
    seg1 = Segment(pt_1=pt5, pt_2=pt6)
    seg2 = Segment(pt_1=pt5, pt_2=pt7)
    print(poly.distance_to_segment(seg1)) # should be 1
    print(poly.distance_to_segment(seg2)) # they intersect

def test_distance_plane():
    print('poly-plane')
    pt1 = Point(-1, 1, 1)
    pt2 = Point(-1, 0, 1)
    pt3 = Point(1, 0, 1)
    pt4 = Point(0, 1, 2)
    pt5 = Point(0, 0, 2)
    pt6 = Point(1, 0, 2)
    pt7 = Point(-1, 0, -2)
    poly = PolygonRegular(vertices=[pt1, pt2, pt3])
    plane1 = Plane(pt_1=pt4, pt_2=pt5, pt_3=pt6)
    plane2 = Plane(pt_1=pt4, pt_2=pt5, pt_3=pt7)
    print(poly.distance_to_plane(plane1)) # should be 1
    print(poly.distance_to_plane(plane2)) # they intersect

def test_distance_polygon():
    print('poly-poly')
    pt1 = Point(-1, 1, 1)
    pt2 = Point(-1, 0, 1)
    pt3 = Point(1, 0, 1)
    pt4 = Point(0, -1, 1)
    pt5 = Point(0, -1, 0)
    pt6 = Point(0, 1, 0)
    pt7 = Point(2, -1, 1)
    pt8 = Point(2, -1, 0)
    pt9 = Point(2, 1, 0)
    poly1 = PolygonRegular(vertices=[pt1, pt2, pt3])
    poly2 = PolygonRegular(vertices=[pt4, pt5, pt6])
    poly3 = PolygonRegular(vertices=[pt7, pt8, pt9])
    print(poly1.distance_to_polygon(poly2)) # they intersect
    print(poly1.distance_to_polygon(poly3)) # should be 1

def test_distance_prism():
    print('poly-prism')


def test_distances():
    print('start testing distances from poly to others...\n')
    test_distance_point()
    test_distance_line()
    test_distance_segment()
    test_distance_plane()
    test_distance_polygon()
    test_distance_prism()
    print('\nfinished')


test_distances()
