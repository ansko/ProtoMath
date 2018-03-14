#!/usr/bin/env python3


from geometry_primitives_line import Line                      # +
from geometry_primitives_plane import Plane                    # +
from geometry_primitives_point import Point                    # +
from geometry_primitives_polygon_regular import PolygonRegular # -
from geometry_primitives_prism_regular import PrismRegular     # -
from geometry_primitives_segment import Segment                # +

from linalg_matrix2 import Matrix2 # +
from linalg_matrix3 import Matrix3 # +
from linalg_matrix4 import Matrix4 # +
from linalg_vector import Vector   # +


print('imports ok')


def test_inits():
    print('pt...')
    pt = Point(0, 0, 0)
    print('pt ok')

    print('vec...')
    vec = Vector(1, 1, 1)
    print('vec ok')

    print('m2...')
    m21 = Matrix2(a11=0, a12=0, a21=0, a22=0)
    print('1 ok')
    m22 = Matrix2(elements=[0, 0, 0, 0])
    print('2 ok')
    print('m2 ok')


    print('m3...')
    m31 = Matrix3(a11=0, a12=0, a13=0,
                  a21=0, a22=0, a23=0,
                  a31=0, a32=0, a33=0)
    print('1 ok')
    m32 = Matrix3(elements=[0, 0, 0, 0, 0, 0, 0, 0, 0])
    print('2 ok')
    print('m3 ok')

    print('m4...')
    m41 = Matrix4(a11=0, a12=0, a13=0, a14=0,
                  a21=0, a22=0, a23=0, a24=0,
                  a31=0, a32=0, a33=0, a34=0,
                  a41=0, a42=0, a43=0, a44=0)
    print('1 ok')
    m42 = Matrix4(elements=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    print('2 ok')
    print('m4 ok')

    print('line...')
    line1 = Line(pt_1=Point(0, 0, 0), pt_2=Point(1, 1, 1))
    print('1 ok')
    #line2 = Line(plane_1=None, plane_2=None)
    print('line ok')

    print('seg')
    segment=Segment(beg=Point(0, 0, 0), end=Point(1, 1, 1))
    print('seg ok')

    print('plane')
    plane1 = Plane(a=1, b=1, c=1, d=1)
    print('1 ok')
    plane2 = Plane(pt_1=Point(0, 0, 0), pt_2=Point(0, 0, 1), pt_3=Point(0, 1, 0))
    print('2 ok')
    plane3 = Plane(pt=Point(0, 0, 0), normal=Vector(1, 1, 1))
    print('3 ok')
    plane4 = Plane(pt=Point(0, 0, 0), 
                   segment=Segment(beg=Point(0, 0, 1), end=Point(1, 1, 1)))
    print('4 ok')
    print('plane ok')

    print('poly_reg')
    polygon_reg1 = PolygonRegular(vertices=(Point(0, 0, 0),
                                            Point(1, 0, 0),
                                            Point(0, 1, 0),
                                            Point(1, 1, 0)))
    print('poly_reg ok')

    print('prism_reg')
    prism_reg1 = PrismRegular(top_facet=polygon_reg1,
                              bot_facet=PolygonRegular(vertices=(Point(0, 0, 1),
                                                                 Point(1, 0, 1),
                                                                 Point(0, 1, 1),
                                                                 Point(1, 1, 1))))
    print('prism_reg ok')


test_inits()
