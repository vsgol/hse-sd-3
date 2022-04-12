from dune_rogue.logic.entities.npcs.cielago import Cielago
from dune_rogue.logic.entities.player_character import PlayerCharacter
from dune_rogue.logic.entities.static_entities import WallEntity, FloorEntity, LevelFinishEntity


class EntityFactory:
    """Entities factory"""
    @staticmethod
    def create_player_character(x, y):
        """Created player character entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized character entity
        """
        return PlayerCharacter(x, y)

    @staticmethod
    def create_wall(x, y):
        """Created wall entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized wall entity
        """
        return WallEntity(x, y)

    @staticmethod
    def create_floor(x, y):
        """Created floor entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized floor entity
        """
        return FloorEntity(x, y)

    @staticmethod
    def create_finish(x, y):
        """Created finish entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized finish entity
        """
        return LevelFinishEntity(x, y)

    @staticmethod
    def create_cielago(x, y):
        return Cielago(x, y)
