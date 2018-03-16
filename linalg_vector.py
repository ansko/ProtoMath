class Vector:
    def __init__(self,
                       x=None, y=None, z=None,
                       pt_1=None, pt_2=None,
                       segment=None):
        if not None in (x, y, z):
            self.x = x
            self.y = y
            self.z = z
        elif not None in (pt_1, pt_2):
            self.x = pt_2.x - pt_1.x
            self.y = pt_2.y - pt_1.y
            self.z = pt_2.z - pt_1.z
        elif segment is not None:
            self.x = segment.dx()
            self.y = segment.dy()
            self.z = segment.dz()
        else:
            print('error in vector init:',
                  'incorrect arguments')
            return None
        if self.x == 0 and self.y == 0 and self.z == 0:
            #import sys
            #print('aaaa')
            #sys.exit()
            pass


    """
        Other special methods.
    """
    def __str__(self):
        return 'vec(' + str(self.x) + ', ' + str(self.y) + '. ' + str(self.z) + ')'

    def __neg__(self):
        return Vector(x=-self.x, y=-self.y, z=-self.z)


    """
        A group of methods to get vector's properties.
    """
    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def product_with(self, vec):
        return self.x * vec.x + self.y * vec.y + self.z * vec.z

    def vector_product_with(self, vec):
        x = self.y * vec.z - self.z * vec.y
        y = -self.x * vec.z + self.z * vec.x
        z = self.x * vec.y - self.y * vec.x
        return Vector(x=x, y=y, z=z)

    """
        A group of methods to change vector.
    """
    def multiply_by_number(self, number):
        if number == 0:
            print('warning:',
                  'vector multiply_by_number: number is 0!')
        self.x *= number
        self.y *= number
        self.z *= number

    def divide_by_number(self, number):
        if number == 0:
            print('error:',
                  'vector divide_by_number: number is 0!')
            return None
        self.x /= number
        self.y /= number
        self.z /= number

    def add_vector(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

    def substract_vector(self, vector):
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z

    def renorm(self, length=1):
        """
            Make vector have given length.
        """
        self.multiply_by_number(length / self.length())
