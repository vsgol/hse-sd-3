from abc import ABC

from dune_rogue.logic.coordinate import Coordinate


class GameEntity(ABC):
    """Game entity abstract class"""
    def __init__(self, x, y, is_solid, glyph, is_alive=True, is_player=False):
        """
        :param x: entity x coobehaviorrdinate
        :param y: entity y coordinate
        :param is_solid: flag whether other entities can share position with this one
        :param glyph: glyph for scene rendering
        :param is_alive: flag whether entity exists
        :param is_player: flag whether entity is a player character
        """
        self.coord = Coordinate(x, y)
        self.is_solid = is_solid
        self.glyph = glyph
        self.is_alive = is_alive
        self.is_player = is_player

    @property
    def x(self):
        return self.coord.x

    @property
    def y(self):
        return self.coord.y

    @x.setter
    def x(self, value):
        self.coord.x = value

    @y.setter
    def y(self, value):
        self.coord.y = value

    def intersect(self, other):
        """Handler for entities intersection
        :argument other: entity which intersected
        """
        pass

    def __str__(self):
        return self.glyph.symbol
