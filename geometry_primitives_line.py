from linalg_vector import Vector


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
