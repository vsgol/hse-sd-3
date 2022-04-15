from dune_rogue.logic.entities.items.unfixed_crysknife_entity import UnfixedCrysknifeEntity
from dune_rogue.logic.entities.items.worn_stillsuit_entity import WornStillsuitEntity
from dune_rogue.logic.entities.npcs.cielago import Cielago
from dune_rogue.logic.entities.npcs.kangaroo_mouse import KangarooMouse
from dune_rogue.logic.entities.npcs.kit_fox import KitFox
from dune_rogue.logic.entities.player_character import PlayerCharacter
from dune_rogue.logic.entities.static_entities import WallEntity, FloorEntity, LevelFinishEntity
from dune_rogue.logic.items.armors.worn_stillsuit import WornStillsuit
from dune_rogue.logic.items.weapons.unfixed_crysknife import UnfixedCrysknife


class EntityFactory:
    """Entities factory"""
    @staticmethod
    def create_player_character(x, y):
        """Created player character entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized character entity
        """
        player = PlayerCharacter(x, y)
        return player

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

    @staticmethod
    def create_mouse(x, y):
        return KangarooMouse(x, y)

    @staticmethod
    def create_fox(x, y):
        return KitFox(x, y)

    @staticmethod
    def create_unfixed_crys(x, y):
        return UnfixedCrysknifeEntity(x, y)

    @staticmethod
    def create_worn_stillsuit(x, y):
        return WornStillsuitEntity(x, y)
