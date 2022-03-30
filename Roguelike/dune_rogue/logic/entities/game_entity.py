from abc import ABC


class GameEntity(ABC):
    """Game entity abstract class"""
    def __init__(self, x, y, is_solid, glyph, is_alive=True):
        """
        :param x: entity x coordinate
        :param y: entity y coordinate
        :param is_solid: flag whether other entities can share position with this one
        :param glyph: glyph for scene rendering
        :param is_alive: flag whether entity exists
        """
        self.x = x
        self.y = y
        self.is_solid = is_solid
        self.glyph = glyph
        self.is_alive = is_alive

    def intersect(self, other):
        """Handler for entities intersection
        :argument other: entity which intersected
        """
        pass

    def __str__(self):
        return self.glyph.symbol
