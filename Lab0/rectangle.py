class Rectangle(object):
    """Rectangle class"""

    def __init__(self, width=1, height=2):
        self.width = width
        self.height = height

    def area(self):
        """ Returns the area of the rectangle """
        return self.width * self.height

    def perimeter(self):
        """ Returns the perimeter of the rectangle """
        return 2 * (self.width + self.height)

    def __str__(self):
        """ return string representation of the rectangle """
        result = "#" * self.width + "\n"
        return result * self.height


not_square = Rectangle()
is_square = Rectangle(2, 2)

my_rec = Rectangle(3, 4)
print(my_rec.area())
print(my_rec.perimeter())

my_rec = Rectangle()
print(my_rec.perimeter())


recker = Rectangle(2, 3)
print(recker)

recker = Rectangle(20, 5)
print(recker)
