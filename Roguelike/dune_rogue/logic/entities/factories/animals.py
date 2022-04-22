from dune_rogue.logic.entities.factories.factory import EntityFactory
from dune_rogue.logic.entities.items.unfixed_crysknife_entity import UnfixedCrysknifeEntity
from dune_rogue.logic.entities.items.worn_stillsuit_entity import WornStillsuitEntity
from dune_rogue.logic.entities.npcs.cielago import Cielago
from dune_rogue.logic.entities.npcs.kangaroo_mouse import KangarooMouse
from dune_rogue.logic.entities.npcs.kit_fox import KitFox


class AnimalsFactory(EntityFactory):
    """Animals factory"""
    @staticmethod
    def create_aggressive(x, y):
        """Creates cielago entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized cielago entity
        """
        return Cielago(x, y)

    @staticmethod
    def create_coward(x, y):
        """Creates kangaroo mouse entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized kangaroo mouse entity
        """
        return KangarooMouse(x, y)

    @staticmethod
    def create_passive(x, y):
        """Creates kit fox entity
        :argument x: Entity x coordinate
        :argument y: Entity y coordinate
        :return: Initialized kit fox entity
        """
        return KitFox(x, y)
