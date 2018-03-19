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
    pt1 = Point(0, 0, 0)
    pt2 = Point(0, 0, 0)
    print('pt-pt')
    print(pt1.distance_to_point(pt1))
    print(pt1.distance_to_point(pt2))

def test_distance_line():
    pt0 = Point(0, 0, 0)
    pt1 = Point(1, 0, 0)
    pt2 = Point(1, 1, 0)
    pt3 = Point(0, 0, 4)
    line = Line(pt_1 = pt1, pt_2 = pt2)
    print('pt-line')
    print(pt0.distance_to_line(line))
    seg = Segment(pt1, pt2)
    print(pt0.distance_to_segment(seg))
    plane = Plane(pt_1=pt0, pt_2=pt1, pt_3=pt2)
    print(pt3.distance_to_plane(plane))

def test_distance_segment():
    print('pt-seg')
    pt0 = Point(0, 0, 0)
    pt1 = Point(-1, 1, 1)
    pt2 = Point(1, 1, 1)
    print(pt0.distance_to_segment(Segment(pt_1=pt1, pt_2=pt2)))

def test_distance_plane():
    print('pt-plane')
    pt0 = Point(1, 1, 1)
    pt1 = Point(-1, 1, 0)
    pt2 = Point(1, 1, 0)
    pt3 = Point(0, 0, 0)
    print(pt0.distance_to_plane(Plane(pt_1=pt1, pt_2=pt2, pt_3=pt3)))

def test_distance_polygon():
    print('pt-poly')
    pt0 = Point(0, 10, 0)
    pt1 = Point(-1, 1, 0)
    pt2 = Point(1, 1, 0)
    pt3 = Point(1, -1, 0)
    pt4 = Point(-1, -1, 0)
    poly = PolygonRegular(vertices=[pt1, pt2, pt3, pt4])
    print(pt0.distance_to_polygon_regular(poly))

def test_distance_prism():
    print('pt-prism')
    pt0 = Point(0, 0, 11)
    pt10 = Point(-1, 1, 0)
    pt20 = Point(1, 1, 0)
    pt30 = Point(1, -1, 0)
    pt40 = Point(-1, -1, 0)
    top = PolygonRegular(vertices=[pt10, pt20, pt30, pt40])
    pt11 = Point(-1, 1, 1)
    pt21 = Point(1, 1, 1)
    pt31 = Point(1, -1, 1)
    pt41 = Point(-1, -1, 1)
    bot = PolygonRegular(vertices=[pt11, pt21, pt31, pt41])
    prism = PrismRegular(top_facet=top, bot_facet=bot)
    print(pt0.distance_to_prism_regular(prism))

def test_distances():
    print('start testing distances from pt to others...\n')
    test_distance_point()
    test_distance_line()
    test_distance_segment()
    test_distance_plane()
    test_distance_polygon()
    test_distance_prism()
    print('\nfinished')


test_distances()
