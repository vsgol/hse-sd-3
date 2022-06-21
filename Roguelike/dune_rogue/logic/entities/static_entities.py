from abc import ABC

from dune_rogue.logic.entities.game_entity import GameEntity
from dune_rogue.render.color import Color, WHITE_COLOR
from dune_rogue.render.glyph import Glyph


class StaticEntity(GameEntity, ABC):
    """Abstract class for static entities"""
    pass


class WallEntity(StaticEntity):
    """Wall entity

    """
    def __init__(self, x, y):
        """
        :param x: x coordinate
        :param y: y coordinate
        """
        super().__init__(x, y, is_solid=True, glyph=Glyph(symbol='#', color=WHITE_COLOR))


class FloorEntity(StaticEntity):
    """Floor entity"""
    def __init__(self, x, y):
        """
        :param x: x coordinate
        :param y: y coordinate
        """
        super().__init__(x, y, is_solid=False, glyph=Glyph(symbol=' ', color=Color(0, 0, 0)))


class LevelFinishEntity(StaticEntity):
    """Level finish entity"""
    def __init__(self, x, y):
        """
        :param x: x coordinate
        :param y: y coordinate
        """
        super().__init__(x, y, is_solid=False, glyph=Glyph(symbol='X', color=Color(255, 0, 0)))
