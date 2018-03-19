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
    pt = Point(0, 0, 0)
    pt1 = Point(1, 0, 0)
    pt2 = Point(-1, 0, 0)
    seg = Segment(pt_1=pt1, pt_2=pt2)
    print(seg.distance_to_point(pt))

def test_distance_line():
    pt1 = Point(1, 0, 1)
    pt2 = Point(-1, 0, 1)
    pt3 = Point(0, -1, 0)
    pt4 = Point(0, 1, 0)
    pt5 = Point(0, -1, 1)
    pt6 = Point(0, 1, 1)
    seg = Segment(pt_1=pt1, pt_2=pt2)
    line1 = Line(pt_1=pt3, pt_2=pt4)
    line2 = Line(pt_1=pt5, pt_2=pt6)
    print(seg.distance_to_line(line1)) # distance should be 1
    print(seg.distance_to_line(line2)) # they cross

def test_distance_segment():
    pt1 = Point(1, 0, 1)
    pt2 = Point(-1, 0, 1)
    pt3 = Point(0, -1, 0)
    pt4 = Point(0, 1, 0)
    pt5 = Point(0, -1, 1)
    pt6 = Point(0, 1, 1)
    seg = Segment(pt_1=pt1, pt_2=pt2)
    seg1 = Segment(pt_1=pt3, pt_2=pt4)
    seg2 = Segment(pt_1=pt5, pt_2=pt6)
    print(seg.distance_to_segment(seg1)) # distance should be 1
    print(seg.distance_to_segment(seg2)) # they cross

def test_distance_plane():
    pt1 = Point(0, 0, 1)
    pt2 = Point(0, 0, -1)
    pt3 = Point(0, 1, 1)
    pt4 = Point(-1, 0, 0)
    pt5 = Point(1, 0, 0)
    pt6 = Point(-1, 0, 1)
    plane = Plane(pt_1=pt1, pt_2=pt2, pt_3=pt3)
    seg1 = Segment(pt_1=pt4, pt_2=pt5)
    seg2 = Segment(pt_1=pt4, pt_2=pt6)
    print(seg1.distance_to_plane(plane)) # they cross
    print(seg2.distance_to_plane(plane)) # distance should be 1

def test_distance_polygon():
    pt1 = Point(0, 0, -1)
    pt2 = Point(0, 0, 1)
    pt3 = Point(0, 1, 1)
    pt4 = Point(0, 1, -1)
    poly = PolygonRegular(vertices=[pt1, pt2, pt3, pt4])
    pt5 = Point(1, 0, 0)
    pt6 = Point(1, 1, 0)
    pt7 = Point(-1, 0, 0)
    pt8 = Point(-1, 0, 100)
    seg1 = Segment(pt_1=pt5, pt_2=pt6)
    seg2 = Segment(pt_1=pt5, pt_2=pt7)
    seg3 = Segment(pt_1=pt5, pt_2=pt8)
    print(seg1.distance_to_polygon(poly)) # should be 1
    print(seg3.distance_to_polygon(poly)) # should be a little bit less than 1
    print(seg2.distance_to_polygon(poly)) # they cross

def test_distance_prism():
    pt10 = Point(0, 0, -1)
    pt20 = Point(0, 0, 1)
    pt30 = Point(0, 1, 1)
    pt40 = Point(0, 1, -1)
    pt11 = Point(1, 0, -1)
    pt21 = Point(1, 0, 1)
    pt31 = Point(1, 1, 1)
    pt41 = Point(1, 1, -1)
    prism = PrismRegular(
        top_facet=PolygonRegular(vertices=[pt10, pt20, pt30, pt40]),
        bot_facet=PolygonRegular(vertices=[pt11, pt21, pt31, pt41]))
    pt1 = Point(0, 0, 0)
    pt2 = Point(2, 0, 0)
    pt3 = Point(3, 0, 0)
    seg1 = Segment(pt1, pt2)
    seg2 = Segment(pt2, pt3)
    print(seg1.distance_to_prism(prism)) # they cross
    print(seg2.distance_to_prism(prism)) # should be 1


def test_distances():
    print('start testing distances from segment to others...\n')
    print('seg-pt')
    test_distance_point()
    print('seg-line')
    test_distance_line()
    print('seg-seg')
    test_distance_segment()
    print('seg-plane')
    test_distance_plane()
    print('seg-poly')
    test_distance_polygon()
    print('seg-prism')
    test_distance_prism()
    print('\nfinished')


test_distances()
