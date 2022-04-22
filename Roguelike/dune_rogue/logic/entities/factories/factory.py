from dune_rogue.logic.entities.items.healing_potion_entity import HealingPotionEntity
from dune_rogue.logic.entities.items.unfixed_crysknife_entity import UnfixedCrysknifeEntity
from dune_rogue.logic.entities.items.worn_stillsuit_entity import WornStillsuitEntity
from dune_rogue.logic.entities.npcs.cielago import Cielago
from dune_rogue.logic.entities.npcs.ghola import Ghola
from dune_rogue.logic.entities.npcs.kangaroo_mouse import KangarooMouse
from dune_rogue.logic.entities.npcs.kit_fox import KitFox
from dune_rogue.logic.entities.player_character import PlayerCharacter
from dune_rogue.logic.entities.static_entities import WallEntity, FloorEntity, LevelFinishEntity
from dune_rogue.logic.items.armors.worn_stillsuit import WornStillsuit
from dune_rogue.logic.items.usable.healing_potion import HealingPotion
from dune_rogue.logic.items.weapons.unfixed_crysknife import UnfixedCrysknife


class EntityFactory:
    """Entities factory"""
    @staticmethod
    def create_player_character(x, y):
        """Creates player character entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized character entity
        """
        player = PlayerCharacter(x, y)
        for _ in range(3):
            player.inventory.add_item(HealingPotion())
        return player

    @staticmethod
    def create_wall(x, y):
        """Creates wall entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized wall entity
        """
        return WallEntity(x, y)

    @staticmethod
    def create_floor(x, y):
        """Creates floor entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized floor entity
        """
        return FloorEntity(x, y)

    @staticmethod
    def create_finish(x, y):
        """Creates finish entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized finish entity
        """
        return LevelFinishEntity(x, y)

    @staticmethod
    def create_aggressive(x, y):
        """Creates aggressive enemy
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized cielago entity
        """
        return Cielago(x, y)

    @staticmethod
    def create_coward(x, y):
        """Creates coward enemy
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized kangaroo mouse entity
        """
        return KangarooMouse(x, y)

    @staticmethod
    def create_passive(x, y):
        """Creates passive enemy
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized kit fox entity
        """
        return KitFox(x, y)

    @staticmethod
    def create_unfixed_crys(x, y):
        """Creates unfixed crysknife entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized unfixed crysknife entity
        """
        return UnfixedCrysknifeEntity(x, y)

    @staticmethod
    def create_worn_stillsuit(x, y):
        """Creates unfixed worn stillsuit entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized worn stillsuit entity
        """
        return WornStillsuitEntity(x, y)

    @staticmethod
    def create_potion(x, y):
        """Creates unfixed worn stillsuit entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized healing potion entity
        """
        return HealingPotionEntity(x, y)

    @staticmethod
    def create_ghola(x, y):
        """Creates ghola entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized ghola entity
        """
        return Ghola(x, y)
