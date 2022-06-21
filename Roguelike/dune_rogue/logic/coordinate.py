class Coordinate:
    """2D vector class"""
    def __init__(self, x=0, y=0):
        """
        :param x: x coordinate
        :param y: x coordinate
        """
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Coordinate(-self.x, -self.y)

    def __sub__(self, other):
        return self + (-other)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
