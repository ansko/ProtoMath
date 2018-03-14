class Vector:
    def __init__(self,
                       x, y, z):
        self.x = x
        self.y = y
        self.z = z


    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5


    def multiply_by_number(self, number):
        if number == 0:
            print('warning:',
                  'Vector.multiply_by_number: number is 0!')
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

    def add_vector(self, vector=None):
        if vector is None:
            print('Error in Vector.add_vector:',
                  'other vector is not specified!')
            return None
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z

    def substract_vector(self, vector=None):
        if vector is None:
            print('error in vector substract_vector:',
                  'other vector is not specified!')
            return None
        self.x -= vector.x
        self.y -= vector.y
        self.z -= vector.z
