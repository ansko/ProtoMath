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
    pt0 = Point(0, 0, 0)
    pt1 = Point(0, 0, 1)
    pt2 = Point(1, 0, 0)
    line = Line(pt_1=pt0, pt_2=pt1)
    print(line.distance_to_point(pt2))  # should be 1

def test_distance_line():
    pt0 = Point(0, 0, 0)
    pt1 = Point(0, 0, 1)
    pt2 = Point(1, 0, 0)
    pt3 = Point(1, 0, 1)
    line1 = Line(pt_1=pt0, pt_2=pt1)
    line2 = Line(pt_1=pt2, pt_2=pt3)
    print(line1.distance_to_line(line2))   # should be 1

def test_distance_segment():
    pt0 = Point(0, 0, 0)
    pt1 = Point(0, 0, 1)
    pt2 = Point(1, 0, 0)
    pt3 = Point(1, 0, 1)
    line = Line(pt_1=pt0, pt_2=pt1)
    seg = Segment(pt_1=pt2, pt_2=pt3)
    print(line.distance_to_segment(seg))  # should be 1

def test_distance_plane():
    pt0 = Point(0, 0, 0)
    pt1 = Point(0, 0, 1)
    pt2 = Point(0, 1, 0)
    pt3 = Point(1, 0, 0)
    pt4 = Point(1, 0, 1)
    pt5 = Point(-1, 0, 10)
    plane = Plane(pt_1=pt0, pt_2=pt1, pt_3=pt2)
    line1 = Line(pt_1=pt3, pt_2=pt4)
    line2 = Line(pt_1=pt3, pt_2=pt5)
    print(line1.distance_to_plane(plane)) # should be 1
    print(line2.distance_to_plane(plane)) # they intersect

def test_distance_polygon():
    pt0 = Point(0, 0, 0)
    pt1 = Point(1, 0, 0)
    pt6 = Point(0, 0, 5)
    pt7 = Point(1, 0, 5)
    pt8 = Point(0, 4, 5)
    pt9 = Point(1, 4, 5)
    pt2 = Point(0, 0, 1)
    pt3 = Point(1, 0, 1)
    pt4 = Point(1, 1, 1)
    pt5 = Point(0, 1, 1)
    line1 = Line(pt_1=pt0, pt_2=pt2)
    line2 = Line(pt_1=pt0, pt_2=pt1)
    line3 = Line(pt_1=pt6, pt_2=pt7)
    line4 = Line(pt_1=pt8, pt_2=pt9)
    poly1 = PolygonRegular(vertices=[pt2, pt3, pt4, pt5])
    print(line1.distance_to_polygon(poly1)) # they intersect
    print(line2.distance_to_polygon(poly1)) # should be 1
    print(line3.distance_to_polygon(poly1)) # should be 4
    print(line4.distance_to_polygon(poly1)) # should be 5

def test_distance_prism():
    pt0 = Point(0, 0, -1)
    pt1 = Point(1, 0, -1)
    pt2 = Point(0, 0, 0)
    pt3 = Point(1, 0, 0)
    pt4 = Point(1, 1, 0)
    pt5 = Point(0, 1, 0)
    pt6 = Point(0, 0, 1)
    pt7 = Point(1, 0, 1)
    pt8 = Point(1, 1, 1)
    pt9 = Point(0, 1, 1)
    pt10 = Point(-4, 0, -3)
    pt11 = Point(-4, 1, -3)
    line1 = Line(pt_1=pt0, pt_2=pt1)
    line2 = Line(pt_1=pt10, pt_2=pt11)
    prism = PrismRegular(top_facet=PolygonRegular(vertices=[pt2, pt3, pt4, pt5]),
                         bot_facet=PolygonRegular(vertices=[pt6, pt7, pt8, pt9]))
    print(line1.distance_to_prism(prism)) # should be 1
    print(line2.distance_to_prism(prism)) # should be 5


def test_distances():
    print('start testing distances from line to others...\n')
    print('line-pt')
    test_distance_point()
    print('line-line')
    test_distance_line()
    print('line-seg')
    test_distance_segment()
    print('line-plane')
    test_distance_plane()
    print('line-polygon')
    test_distance_polygon()
    print('line-prism')
    test_distance_prism()
    print('\nfinished')


test_distances()
